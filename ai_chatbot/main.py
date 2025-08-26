import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from chatbot.handlers import handle_chat, Filters, ChatResult
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="AI Chatbot Service (Grok + OpenAI)")

# CORS configuration with debug logging
cors_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
logger.info(f"🔧 CORS_ENV variable: {cors_env}")

origins = [o.strip() for o in cors_env.split(",")]
logger.info(f"🔧 Initial origins: {origins}")

if origins == ["*"]:
    origins = ["*"]
    logger.info("🔧 Using wildcard CORS (*)")
else:
    # Add common development origins
    origins.extend([
        "http://localhost:3000",
        "http://localhost:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000"
    ])
    logger.info(f"🔧 Extended origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_prompt: str
    top_k: int = 5

@app.post("/chat", response_model=ChatResult)
def chat(req: ChatRequest):
    logger.info(f"🚀 CHAT API CALL - User prompt: {req.user_prompt}")
    logger.info(f"📊 Requested top_k: {req.top_k}")
    
    result = handle_chat(req.user_prompt)
    
    if req.top_k and req.top_k != result.filters.top_k:
        logger.info(f"🔄 Adjusting top_k from {result.filters.top_k} to {req.top_k}")
        result.filters.top_k = req.top_k
    
    logger.info(f"📤 Returning chat result with {result.filters.top_k} jobs")
    return result

@app.post("/parse", response_model=Filters)
def parse(req: ChatRequest):
    logger.info(f"🔍 PARSE API CALL - User prompt: {req.user_prompt}")
    
    res = handle_chat(req.user_prompt)
    
    if req.top_k and req.top_k != res.filters.top_k:
        logger.info(f"🔄 Adjusting top_k from {res.filters.top_k} to {req.top_k}")
        res.filters.top_k = req.top_k
    
    logger.info(f"📤 Returning parsed filters: {res.filters.model_dump_json(indent=2)}")
    return res.filters

@app.get("/health")
def health():
    logger.info("🏥 Health check requested")
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

@app.get("/agent/status")
def agent_status():
    """Check uAgent status without triggering Grok API calls"""
    logger.info("🔍 Agent status check requested")
    return {
        "ready": True,
        "status": "agent_available",
        "message": "uAgent is available for chat requests",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.get("/agent/ready")
def agent_ready():
    """Check if uAgent is ready for chat requests"""
    logger.info("🔍 Agent readiness check requested")
    return {
        "ready": True,
        "status": "ready",
        "message": "uAgent is ready to handle chat requests",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Handle OPTIONS requests explicitly for CORS preflight
@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    logger.info(f"🔧 Handling OPTIONS request for: {full_path}")
    return {"message": "OK"}

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8081"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info("🚀 Starting AI Chatbot Service...")
    logger.info(f"📡 Server will be available at: http://{host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"🤖 Model type: {os.getenv('MODEL_TYPE', 'grok')}")
    logger.info(f"📊 Health check: http://{host}:{port}/health")
    logger.info(f"💬 Chat endpoint: http://{host}:{port}/chat")
    logger.info(f"🌐 Final CORS origins: {origins}")
    logger.info("=" * 50)
    
    # Start the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
