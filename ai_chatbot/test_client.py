#!/usr/bin/env python3
"""
Test client for your upgraded ASI:1 compatible agent
This client will send a test message to your agent using the proper chat protocol
"""

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

# Replace this with your agent's actual address
# You can find this in your agent's startup logs
AI_AGENT_ADDRESS = "your_agent_address_here"  # Replace with actual address

# Create a test client agent
client = Agent(
    name="test-client",
    seed="test_client_seed_for_testing_only",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
)

# Create protocol for the client
protocol = Protocol(spec=chat_protocol_spec)

@client.on_event("startup")
async def send_test_message(ctx: Context):
    """Send a test job request to your agent"""
    print(f"🚀 Test client starting...")
    print(f"📤 Sending test message to: {AI_AGENT_ADDRESS}")
    
    # Send a test job request
    await ctx.send(AI_AGENT_ADDRESS, ChatMessage(
        timestamp=datetime.now(),
        msg_id=uuid4(),
        content=[TextContent(type="text", text="I need a Python developer for a web app project")],
    ))

@client.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgement from your agent"""
    ctx.logger.info(f"✅ Got acknowledgement from {sender} for message {msg.acknowledged_msg_id}")

@client.on_message(ChatMessage)
async def handle_response(ctx: Context, sender: str, msg: ChatMessage):
    """Handle response from your agent"""
    print(f"\n🤖 Response from your agent:")
    
    # Extract text content
    for item in msg.content:
        if isinstance(item, TextContent):
            print(f"📝 {item.text}")
            break
    
    print(f"\n🎉 Chat protocol test successful!")
    print(f"Your agent is now ASI:1 compatible!")

# Include the protocol
client.include(protocol)

if __name__ == "__main__":
    print("🧪 Starting test client for your upgraded agent...")
    print("Make sure your main agent is running first!")
    print("=" * 50)
    client.run()
