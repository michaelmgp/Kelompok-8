from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging
from contextlib import asynccontextmanager

from api.routes import router as api_router
from services.identity_manager import IdentityManager
from agents.coordinator import Coordinator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global services
identity_manager = None
coordinator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global identity_manager, coordinator
    logger.info("Starting up backend services...")
    
    try:
        identity_manager = IdentityManager()
        coordinator = Coordinator()
        logger.info("Backend services started successfully")
    except Exception as e:
        logger.error(f"Failed to start backend services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down backend services...")
    if coordinator:
        await coordinator.cleanup()
    if identity_manager:
        await identity_manager.cleanup()
    logger.info("Backend services shut down successfully")

# Create FastAPI app
app = FastAPI(
    title="Job Platform Backend Agent",
    description="AI-powered job scraping and coordination backend",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Job Platform Backend Agent",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "identity_manager": identity_manager is not None,
            "coordinator": coordinator is not None
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
