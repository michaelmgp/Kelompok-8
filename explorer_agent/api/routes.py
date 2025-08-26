"""
API routes for the Explorer Agent

Defines REST API endpoints for job search and management
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from core.config import get_settings
from core.agent import ExplorerAgent

router = APIRouter()
settings = get_settings()

# Pydantic models for request/response
class JobSearchRequest(BaseModel):
    """Job search request from chatbot conversation"""
    keywords: Optional[str] = ""  # Job title, skills from conversation
    location: Optional[str] = ""  # Location mentioned in chat
    experience_level: Optional[str] = ""  # Junior, Mid, Senior from chat
    job_type: Optional[str] = ""  # Full-time, Part-time, etc.
    industry: Optional[str] = ""  # Industry mentioned
    required_skills: Optional[List[str]] = []  # Skills extracted from conversation
    preferred_companies: Optional[List[str]] = []  # Companies mentioned
    salary_range: Optional[str] = ""  # Salary expectations from chat
    remote_preference: Optional[str] = ""  # Remote, Hybrid, On-site
    limit: Optional[int] = 50
    page: Optional[int] = 1

class JobSearchResponse(BaseModel):
    success: bool
    message: str
    search_id: Optional[str] = None
    total_jobs: Optional[int] = None

class JobData(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: Optional[str] = ""
    requirements: List[str] = []
    salary: Optional[str] = ""
    job_type: Optional[str] = ""
    experience_level: Optional[str] = ""
    posted_date: Optional[str] = ""
    application_url: Optional[str] = ""
    source: str
    scraped_at: str

class AgentStatusResponse(BaseModel):
    is_running: bool
    active_searches: List[str]
    enabled_scrapers: List[str]
    total_scrapers: int

@router.post("/jobs/search")
async def search_jobs(request: JobSearchRequest):
    """Search for jobs based on chatbot conversation parameters"""
    try:
        search_params = {
            "keywords": request.keywords,
            "location": request.location,
            "experience_level": request.experience_level,
            "job_type": request.job_type,
            "industry": request.industry,
            "required_skills": request.required_skills,
            "preferred_companies": request.preferred_companies,
            "salary_range": request.salary_range,
            "remote_preference": request.remote_preference,
            "limit": request.limit,
            "page": request.page
        }
        
        # Filter out empty parameters
        search_params = {k: v for k, v in search_params.items() if v}
        
        # This endpoint is for initiating searches based on chat conversation
        # Actual job streaming happens via WebSocket
        return {
            "success": True,
            "message": f"Job search initiated based on conversation: {request.keywords} in {request.location}",
            "search_params": search_params,
            "websocket_url": "/ws/jobs/stream",
            "conversation_context": "Searching for jobs matching your chat requirements"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/jobs/sources")
async def get_job_sources():
    """Get list of available job sources"""
    sources = []
    
    if settings.enable_linkedin:
        sources.append({
            "name": "LinkedIn",
            "enabled": True,
            "base_url": "https://www.linkedin.com/jobs"
        })
        
    if settings.enable_indeed:
        sources.append({
            "name": "Indeed",
            "enabled": True,
            "base_url": "https://www.indeed.com"
        })
        
    if settings.enable_glassdoor:
        sources.append({
            "name": "Glassdoor",
            "enabled": True,
            "base_url": "https://www.glassdoor.com"
        })
        
    if settings.enable_stackoverflow:
        sources.append({
            "name": "Stack Overflow",
            "enabled": True,
            "base_url": "https://stackoverflow.com/jobs"
        })
        
    return {
        "sources": sources,
        "total_sources": len(sources)
    }

@router.get("/jobs/status")
async def get_job_search_status():
    """Get current job search status"""
    # This would typically get the status from the agent
    # For now, return a placeholder response
    return {
        "status": "idle",
        "message": "No active job searches",
        "last_search": None,
        "total_jobs_found": 0
    }

@router.post("/jobs/analyze")
async def analyze_job(job_data: JobData):
    """Analyze a specific job posting using AI"""
    try:
        # This would typically use the AI processor
        # For now, return a placeholder analysis
        analysis = {
            "job_id": job_data.id,
            "analysis": {
                "skill_match_score": 0.75,
                "experience_level_match": "Good",
                "company_reputation": "Unknown",
                "salary_range_estimate": "Market rate",
                "recommendations": [
                    "Highlight relevant skills in your resume",
                    "Emphasize similar project experience",
                    "Prepare for technical interview questions"
                ]
            },
            "processed_at": "2024-01-01T00:00:00Z"
        }
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/agent/status")
async def get_agent_status():
    """Get the current status of the explorer agent"""
    # This would typically get the status from the agent instance
    # For now, return a placeholder response
    return AgentStatusResponse(
        is_running=False,
        active_searches=[],
        enabled_scrapers=["LinkedIn", "Indeed", "Glassdoor"],
        total_scrapers=3
    )

@router.post("/agent/start")
async def start_agent():
    """Start the explorer agent"""
    try:
        # This would typically start the agent
        return {
            "success": True,
            "message": "Explorer agent started successfully",
            "status": "running"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start agent: {str(e)}")

@router.post("/agent/stop")
async def stop_agent():
    """Stop the explorer agent"""
    try:
        # This would typically stop the agent
        return {
            "success": True,
            "message": "Explorer agent stopped successfully",
            "status": "stopped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop agent: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Explorer Agent",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.get("/config")
async def get_configuration():
    """Get current configuration (non-sensitive)"""
    return {
        "port": settings.port,
        "host": settings.host,
        "debug": settings.debug,
        "rate_limit": settings.rate_limit,
        "enabled_sources": {
            "linkedin": settings.enable_linkedin,
            "indeed": settings.enable_indeed,
            "glassdoor": settings.enable_glassdoor,
            "stackoverflow": settings.enable_stackoverflow
        },
        "ai_enabled": settings.ai_enabled
    }

