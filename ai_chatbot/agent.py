import os
from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    AgentContent, 
    ChatMessage, 
    ChatAcknowledgement, 
    TextContent,
    chat_protocol_spec
)
from dotenv import load_dotenv

# Reuse your REST bot's logic
from chatbot.handlers import handle_chat

load_dotenv()

AGENT_NAME = os.getenv("AGENT_NAME", "job_chat_agent")
AGENT_SEED = os.getenv("AGENT_SEED")  # if None, uAgents will still run but address changes per run
MAILBOX_URL = os.getenv("MAILBOX_URL", "https://agentverse.ai")
MAILBOX_KEY = os.getenv("MAILBOX_KEY")  # optional but recommended for judging

# Track processed messages to prevent duplicates
processed_messages = set()

# Create agent with proper configuration
agent = Agent(
    name=AGENT_NAME,
    seed=AGENT_SEED,
    mailbox=True,
)

# Create a new protocol which is compatible with the chat protocol spec
# This ensures compatibility between agents and ASI:1
protocol = Protocol(spec=chat_protocol_spec)

@agent.on_event("startup")
async def on_start(ctx: Context):
    if MAILBOX_KEY:
        # uAgents reads this var for mailbox auth
        os.environ["UAGENTS_MAILBOX_KEY"] = MAILBOX_KEY
        ctx.logger.info("Mailbox enabled; your agent is discoverable on Agentverse.")
    ctx.logger.info(f"Agent address: {agent.address}")

# Define the handler for chat messages that are sent to your agent
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    """
    ASI:1 compatible chat protocol handler.
    Processes job search requests and returns structured responses.
    Keeps conversation open until user explicitly ends it.
    """
    # Prevent duplicate message processing
    message_id = str(msg.msg_id)
    if message_id in processed_messages:
        ctx.logger.info(f"Duplicate message detected: {message_id}, skipping...")
        return
    
    # Mark message as processed
    processed_messages.add(message_id)
    ctx.logger.info(f"Processing message: {message_id} from {sender}")
    
    # Send the acknowledgement for receiving the message
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(), 
            acknowledged_msg_id=msg.msg_id
        ),
    )

    # Collect up all the text chunks
    text = ''
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text

    ctx.logger.info(f"Received text: {text}")

    # Check if user wants to end the conversation
    end_conversation_keywords = [
        "goodbye", "bye", "end", "stop", "quit", "exit", 
        "that's all", "thank you", "thanks", "done",
        "finish", "complete", "no more questions"
    ]
    
    user_wants_to_end = any(keyword in text.lower() for keyword in end_conversation_keywords)

    # Process the job request using your existing chatbot logic
    try:
        result = handle_chat(text)
        response = result.message + "\n\n(Use our web app to view the job list panel.)"
        
        # Add conversation guidance if not ending
        if not user_wants_to_end:
            response += "\n\n💡 You can ask me more questions about job searches, or say 'goodbye' to end our conversation."
        else:
            response += "\n\n👋 Thank you for using our job search service! Have a great day!"
            
    except Exception as e:
        ctx.logger.exception('Error processing job request')
        response = "I'm sorry, I encountered an error processing your job request. Please try again."

    ctx.logger.info(f"Sending response: {response[:100]}...")

    # Send the response back to the user with proper chat protocol format
    # No EndSessionContent - keeps conversation open
    await ctx.send(sender, ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=[
            # We send the contents back in the chat message
            TextContent(type="text", text=response),
            # No EndSessionContent - conversation stays open
        ]
    ))
    
    ctx.logger.info(f"Response sent successfully to {sender}")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    # We are not interested in the acknowledgements for this example, but they can be useful to
    # implement read receipts, for example.
    pass

# Attach the protocol to the agent
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()