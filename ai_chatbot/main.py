import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from chatbot.handlers import (
    handle_chat, 
    handle_chat_with_profile,
    Filters, 
    ChatResult,
    set_icp_integration
)
from chatbot.icp_integration import ICPIntegration
from chatbot.user_management import UserManager, MockUserManager, UserProfileInput, VerificationInput
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="AI Chatbot Service (Grok + OpenAI + ICP Integration)")

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
    user_principal: Optional[str] = None  # ICP user principal for personalization

class PersonalizedChatRequest(BaseModel):
    user_prompt: str
    user_principal: str  # Required for personalized responses
    top_k: int = 5

# Initialize ICP integration
icp_integration = None
user_manager = None

try:
    # Get ICP configuration from environment
    identity_canister_id = os.getenv("ICP_IDENTITY_CANISTER_ID")
    chat_canister_id = os.getenv("ICP_CHAT_CANISTER_ID")
    icp_network_url = os.getenv("ICP_NETWORK_URL", "https://ic0.app")
    
    if identity_canister_id and chat_canister_id and identity_canister_id != "mock" and chat_canister_id != "mock":
        logger.info("🔗 Initializing ICP integration...")
        logger.info(f"   Identity Canister: {identity_canister_id}")
        logger.info(f"   Chat Canister: {chat_canister_id}")
        logger.info(f"   Network: {icp_network_url}")
        
        # Note: In production, you'd initialize the ICP agent here
        # For now, we'll create a mock integration
        from chatbot.icp_integration import ICPIntegration
        icp_integration = ICPIntegration(identity_canister_id, chat_canister_id, None)
        set_icp_integration(icp_integration)
        
        # Initialize user manager
        user_manager = UserManager(icp_integration)
        logger.info("✅ ICP integration and user manager initialized")
    else:
        logger.warning("⚠️ ICP canister IDs not configured or using mock mode, running without ICP integration")
        # Use mock user manager for testing
        user_manager = MockUserManager()
        logger.info("🤖 Using mock user manager for testing")
        
except Exception as e:
    logger.error(f"❌ Failed to initialize ICP integration: {e}")
    logger.info("🔄 Running without ICP integration")
    # Use mock user manager as fallback
    user_manager = MockUserManager()

@app.post("/chat", response_model=ChatResult)
async def chat(req: ChatRequest):
    """Standard chat endpoint"""
    logger.info(f"🚀 CHAT API CALL - User prompt: {req.user_prompt}")
    logger.info(f"📊 Requested top_k: {req.top_k}")
    
    result = handle_chat(req.user_prompt)
    
    if req.top_k and req.top_k != result.filters.top_k:
        logger.info(f"🔄 Adjusting top_k from {result.filters.top_k} to {req.top_k}")
        result.filters.top_k = req.top_k
    
    logger.info(f"📤 Returning chat result with {result.filters.top_k} jobs")
    return result

@app.post("/chat/personalized", response_model=ChatResult)
async def personalized_chat(req: PersonalizedChatRequest):
    """Personalized chat endpoint with ICP user profile integration"""
    logger.info(f"🎯 PERSONALIZED CHAT API CALL")
    logger.info(f"👤 User Principal: {req.user_principal}")
    logger.info(f"💬 User prompt: {req.user_prompt}")
    logger.info(f"📊 Requested top_k: {req.top_k}")
    
    if not req.user_principal:
        raise HTTPException(status_code=400, detail="user_principal is required for personalized chat")
    
    if not icp_integration:
        logger.warning("⚠️ ICP integration not available, falling back to standard chat")
        result = handle_chat(req.user_prompt)
        result.personalized = False
        return result
    
    try:
        result = await handle_chat_with_profile(req.user_prompt, req.user_principal)
        
        if req.top_k and req.top_k != result.filters.top_k:
            logger.info(f"🔄 Adjusting top_k from {result.filters.top_k} to {req.top_k}")
            result.filters.top_k = req.top_k
        
        logger.info(f"📤 Returning personalized chat result with {result.filters.top_k} jobs")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in personalized chat: {e}")
        # Fallback to standard chat
        result = handle_chat(req.user_prompt)
        result.personalized = False
    return result

@app.post("/parse", response_model=Filters)
def parse(req: ChatRequest):
    """Parse user prompt into filters"""
    logger.info(f"🔍 PARSE API CALL - User prompt: {req.user_prompt}")
    
    res = handle_chat(req.user_prompt)
    
    if req.top_k and req.top_k != res.filters.top_k:
        logger.info(f"🔄 Adjusting top_k from {res.filters.top_k} to {req.top_k}")
        res.filters.top_k = req.top_k
    
    logger.info(f"📤 Returning parsed filters: {res.filters.model_dump_json(indent=2)}")
    return res.filters

@app.get("/health")
def health():
    """Health check endpoint"""
    logger.info("🏥 Health check requested")
    
    health_status = {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0",
        "features": {
            "grok_integration": True,
            "icp_integration": icp_integration is not None,
            "personalization": icp_integration is not None
        }
    }
    
    if icp_integration:
        health_status["icp"] = {
            "identity_canister": icp_integration.identity_canister_id,
            "chat_canister": icp_integration.chat_canister_id
        }
    
    return health_status

@app.get("/user/profile/{user_principal}")
async def get_user_profile(user_principal: str):
    """Get user profile from ICP identity contract"""
    if not icp_integration:
        raise HTTPException(status_code=503, detail="ICP integration not available")
    
    try:
        logger.info(f"👤 Fetching profile for user: {user_principal}")
        profile = await icp_integration.get_user_profile(user_principal)
        
        if profile:
            return {
                "found": True,
                "profile": profile.__dict__
            }
        else:
            return {
                "found": False,
                "message": "User profile not found"
            }
            
    except Exception as e:
        logger.error(f"❌ Error fetching user profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch user profile: {str(e)}")

@app.get("/user/chats/{user_principal}")
async def get_user_chats(user_principal: str):
    """Get user's chat history from ICP chat contract"""
    if not icp_integration:
        raise HTTPException(status_code=503, detail="ICP integration not available")
    
    try:
        logger.info(f"📚 Fetching chat history for user: {user_principal}")
        chats = await icp_integration.get_user_chat_history(user_principal)
        
        return {
            "user_principal": user_principal,
            "chat_count": len(chats),
            "chats": [chat.__dict__ for chat in chats]
        }
        
    except Exception as e:
        logger.error(f"❌ Error fetching user chats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch user chats: {str(e)}")

# User Management Endpoints
@app.post("/user/profile")
async def create_user_profile(profile_data: UserProfileInput, user_principal: str):
    """Create or update user profile in ICP identity canister"""
    if not user_manager:
        raise HTTPException(status_code=503, detail="User management not available")
    
    try:
        logger.info(f"👤 Creating/updating profile for user: {user_principal}")
        
        # Create or update profile
        result = await user_manager.create_user_profile(user_principal, profile_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "profile_id": result["profile_id"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating user profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create user profile: {str(e)}")

@app.put("/user/profile/{user_principal}")
async def update_user_profile(user_principal: str, profile_data: UserProfileInput):
    """Update existing user profile"""
    if not user_manager:
        raise HTTPException(status_code=503, detail="User management not available")
    
    try:
        logger.info(f"🔄 Updating profile for user: {user_principal}")
        
        result = await user_manager.update_user_profile(user_principal, profile_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "profile_id": result["profile_id"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating user profile: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update user profile: {str(e)}")

@app.post("/user/verification")
async def submit_verification(verification_data: VerificationInput, user_principal: str):
    """Submit verification request for user"""
    if not user_manager:
        raise HTTPException(status_code=503, detail="User management not available")
    
    try:
        logger.info(f"🔍 Submitting verification for user: {user_principal}")
        
        result = await user_manager.submit_verification(user_principal, verification_data)
        
        if result["success"]:
            return {
                "success": True,
                "verification_id": result["verification_id"],
                "message": result["message"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error submitting verification: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit verification: {str(e)}")

@app.get("/user/verifications/{user_principal}")
async def get_user_verifications(user_principal: str):
    """Get all verifications for a user"""
    if not user_manager:
        raise HTTPException(status_code=503, detail="User management not available")
    
    try:
        logger.info(f"📋 Fetching verifications for user: {user_principal}")
        
        result = await user_manager.get_user_verifications(user_principal)
        
        if result["success"]:
            return {
                "user_principal": user_principal,
                "verifications": result["verifications"],
                "count": result["count"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching verifications: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch verifications: {str(e)}")

@app.post("/user/reputation")
async def add_reputation(target_user: str, job_id: str, rating: float, review: str, user_principal: str):
    """Add reputation/review for a user"""
    if not user_manager:
        raise HTTPException(status_code=503, detail="User management not available")
    
    try:
        logger.info(f"⭐ Adding reputation for user: {target_user} by {user_principal}")
        
        # Validate rating
        if rating < 1.0 or rating > 5.0:
            raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 5.0")
        
        result = await user_manager.add_reputation(target_user, job_id, rating, review)
        
        if result["success"]:
            return {
                "success": True,
                "reputation_id": result["reputation_id"],
                "message": result["message"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error adding reputation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add reputation: {str(e)}")

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
    
    logger.info("🚀 Starting AI Chatbot Service with ICP Integration...")
    logger.info(f"📡 Server will be available at: http://{host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"🤖 Model type: {os.getenv('MODEL_TYPE', 'grok')}")
    logger.info(f"🔗 ICP Integration: {'Enabled' if icp_integration else 'Disabled'}")
    logger.info(f"📊 Health check: http://{host}:{port}/health")
    logger.info(f"💬 Chat endpoint: http://{host}:{port}/chat")
    logger.info(f"🎯 Personalized chat: http://{host}:{port}/chat/personalized")
    logger.info(f"👤 User profile: http://{host}:{port}/user/profile/{{principal}}")
    logger.info(f"📚 User chats: http://{host}:{port}/user/chats/{{principal}}")
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
