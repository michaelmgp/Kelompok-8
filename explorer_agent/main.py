"""
Main entry point for the Explorer Agent

Runs the FastAPI server with WebSocket support for real-time job streaming
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import get_settings
from core.agent import ExplorerAgent
from api.routes import router as api_router
from streamers.websocket_manager import WebSocketManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global WebSocket manager
websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Explorer Agent...")
    settings = get_settings()
    
    # Initialize the explorer agent
    app.state.agent = ExplorerAgent()
    await app.state.agent.initialize()
    
    logger.info(f"Explorer Agent started on port {settings.port}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Explorer Agent...")
    await app.state.agent.cleanup()

# Create FastAPI app
app = FastAPI(
    title="Explorer Agent",
    description="An intelligent agent that explores the internet for job listings",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Explorer Agent is running",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

@app.websocket("/ws/jobs/stream")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time job streaming based on chatbot conversation"""
    await websocket_manager.connect(websocket)
    
    try:
        while True:
            # Receive JSON data with search parameters from chatbot
            data = await websocket.receive_json()
            
            if data.get("command") == "start_search":
                # Start job exploration based on chatbot conversation
                search_params = data.get("search_params", {})
                
                # Log the search context from chatbot
                if search_params:
                    logger.info(f"🔍 Starting job search based on chat conversation:")
                    logger.info(f"   Keywords: {search_params.get('keywords', 'N/A')}")
                    logger.info(f"   Location: {search_params.get('location', 'N/A')}")
                    logger.info(f"   Skills: {search_params.get('required_skills', [])}")
                    logger.info(f"   Experience: {search_params.get('experience_level', 'N/A')}")
                    logger.info(f"   Companies: {search_params.get('preferred_companies', [])}")
                
                # Start exploration with specific parameters
                asyncio.create_task(
                    app.state.agent.explore_jobs(websocket, search_params)
                )
                
            elif data.get("command") == "stop_search":
                # Stop job exploration
                await websocket_manager.send_personal_message(
                    "Search stopped", websocket
                )
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        websocket_manager.disconnect(websocket)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

