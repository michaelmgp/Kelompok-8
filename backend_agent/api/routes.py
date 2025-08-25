from fastapi import APIRouter, HTTPException, Depends, Query, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, validator
from datetime import datetime
import logging
import uuid
import time

from services.identity_manager import IdentityManager
from agents.coordinator import Coordinator, UnifiedJob

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Pydantic models matching the exact JSON schema specifications

class SearchRequest(BaseModel):
    """Search request matching the specified JSON schema"""
    skills: List[str] = Field(default=[], description="Required skills")
    keywords: List[str] = Field(default=[], description="Search keywords")
    budget_min: Optional[int] = Field(None, description="Minimum budget")
    budget_max: Optional[int] = Field(None, description="Maximum budget")
    rate_type: Optional[Literal["fixed", "hourly"]] = Field(None, description="Rate type")
    remote: Optional[bool] = Field(None, description="Remote work preference")
    duration_days_max: Optional[int] = Field(None, description="Maximum project duration in days")
    top_k: int = Field(default=5, ge=1, le=50, description="Top K results")
    
    location: Optional[str] = Field(None, description="e.g., 'Jakarta', 'Remote-Only'")
    currency: Optional[str] = Field(None, description="ISO 4217, e.g., 'USD','IDR'")
    sources: List[Literal["upwork", "fiverr", "linkedin", "glints", "other"]] = Field(
        default=["upwork", "fiverr"], 
        description="Platform sources to search"
    )
    sort_by: Literal["relevance", "recent", "budget_desc", "budget_asc"] = Field(
        default="relevance", 
        description="Sorting criteria"
    )
    cursor: Optional[str] = Field(None, description="Opaque pagination cursor")
    page_size: int = Field(default=20, ge=1, le=50, description="Results per page")

    @validator('budget_max')
    def validate_budget_range(cls, v, values):
        if v is not None and 'budget_min' in values and values['budget_min'] is not None:
            if v < values['budget_min']:
                raise ValueError('budget_max must be greater than or equal to budget_min')
        return v

class JobProvenance(BaseModel):
    """Job provenance information"""
    fetched_at: str = Field(description="ISO 8601 timestamp")
    source_url: Optional[str] = Field(None, description="Original source URL")
    raw_excerpt: Optional[str] = Field(None, description="Raw excerpt from source")

class Job(BaseModel):
    """Normalized job object matching the specified JSON schema"""
    id: str = Field(description="Global stable id: <source>:<source_id>")
    source: Literal["upwork", "fiverr", "linkedin", "glints", "other"] = Field(description="Job source platform")
    source_id: str = Field(description="Original source ID")
    title: str = Field(description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    url: str = Field(description="Job URL")
    description: Optional[str] = Field(None, description="Job description")
    
    skills: List[str] = Field(default=[], description="Required skills")
    keywords: List[str] = Field(default=[], description="Job keywords")
    
    rate_type: Optional[Literal["fixed", "hourly"]] = Field(None, description="Rate type")
    budget_min: Optional[float] = Field(None, description="Minimum budget")
    budget_max: Optional[float] = Field(None, description="Maximum budget")
    currency: Optional[str] = Field(None, description="Currency code")
    
    remote: Optional[bool] = Field(None, description="Remote work option")
    location: Optional[str] = Field(None, description="Job location")
    
    duration_days_est: Optional[int] = Field(None, description="Estimated duration in days")
    
    posted_at: Optional[str] = Field(None, description="ISO 8601 posted timestamp")
    updated_at: Optional[str] = Field(None, description="ISO 8601 updated timestamp")
    source_rating: Optional[float] = Field(None, description="Seller/client rating if available")
    
    provenance: Optional[JobProvenance] = Field(None, description="Job provenance information")
    score: Optional[float] = Field(None, ge=0, le=1, description="Relevance score 0..1")

class SearchResponseMeta(BaseModel):
    """Search response metadata"""
    request_id: str = Field(description="Unique request identifier")
    sources_hit: List[str] = Field(description="Sources that returned results")
    took_ms: int = Field(description="Search execution time in milliseconds")
    limits: Dict[str, Any] = Field(
        default_factory=dict,
        description="Rate limiting information"
    )

class SearchResponse(BaseModel):
    """Search response matching the specified JSON schema"""
    jobs: List[Job] = Field(description="List of matching jobs")
    next_cursor: Optional[str] = Field(None, description="Next page cursor")
    meta: SearchResponseMeta = Field(description="Response metadata")

# Legacy models for backward compatibility (can be removed later)
class JobSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for jobs")
    category: Optional[str] = Field(None, description="Job category")
    skills: Optional[List[str]] = Field(None, description="Required skills")
    limit_per_platform: Optional[int] = Field(25, description="Jobs per platform")
    platforms: Optional[List[str]] = Field(["upwork", "fiverr"], description="Platforms to search")

class JobResponse(BaseModel):
    id: str
    platform: str
    title: str
    description: str
    budget: Optional[str]
    skills: List[str]
    category: str
    posted_date: datetime
    url: str
    ai_score: float
    platform_specific_data: Dict[str, Any]
    created_at: datetime

class UserProfile(BaseModel):
    user_id: str
    username: str
    email: str
    skills: List[str]
    experience_level: str
    preferred_platforms: List[str]
    created_at: datetime
    updated_at: datetime

class ProposalRequest(BaseModel):
    job_id: str
    cover_letter: str
    proposed_budget: Optional[str]
    delivery_time: Optional[str]
    portfolio_links: Optional[List[str]]

# Dependency injection
async def get_coordinator() -> Coordinator:
    """Get coordinator instance from main app"""
    from main import coordinator
    if not coordinator:
        raise HTTPException(status_code=503, detail="Coordinator not available")
    return coordinator

async def get_identity_manager() -> IdentityManager:
    """Get identity manager instance from main app"""
    from main import identity_manager
    if not identity_manager:
        raise HTTPException(status_code=503, detail="Identity manager not available")
    return identity_manager

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Get current user from JWT token"""
    # This would validate JWT and return user ID
    # For now, just return a placeholder
    return "user_123"

def _convert_unified_job_to_normalized(unified_job: UnifiedJob) -> Job:
    """Convert UnifiedJob to normalized Job format"""
    # Extract source and source_id from the unified ID
    if ":" in unified_job.id:
        source, source_id = unified_job.id.split(":", 1)
    else:
        source = unified_job.platform
        source_id = unified_job.id
    
    # Parse budget information
    budget_min = None
    budget_max = None
    currency = None
    if unified_job.budget:
        # Simple budget parsing - in production, use proper currency detection
        budget_str = str(unified_job.budget)
        if "$" in budget_str:
            currency = "USD"
            try:
                budget_value = float(budget_str.replace("$", "").replace(",", ""))
                budget_min = budget_value
                budget_max = budget_value
            except:
                pass
    
    # Determine rate type based on platform and data
    rate_type = None
    if unified_job.platform == "upwork":
        rate_type = "fixed"  # Upwork typically has fixed projects
    elif unified_job.platform == "fiverr":
        rate_type = "fixed"  # Fiverr gigs are typically fixed price
    
    # Extract additional data from platform_specific_data
    source_rating = None
    if unified_job.platform == "fiverr" and "rating" in unified_job.platform_specific_data:
        source_rating = unified_job.platform_specific_data.get("rating")
    
    # Create provenance
    provenance = JobProvenance(
        fetched_at=datetime.utcnow().isoformat() + "Z",
        source_url=unified_job.url,
        raw_excerpt=unified_job.description[:200] if unified_job.description else None
    )
    
    return Job(
        id=unified_job.id,
        source=source,
        source_id=source_id,
        title=unified_job.title,
        company=None,  # Not available in current UnifiedJob
        url=unified_job.url,
        description=unified_job.description,
        skills=unified_job.skills or [],
        keywords=[],  # Not available in current UnifiedJob
        rate_type=rate_type,
        budget_min=budget_min,
        budget_max=budget_max,
        currency=currency,
        remote=True,  # Assume remote for freelance platforms
        location=None,
        duration_days_est=None,  # Not available in current UnifiedJob
        posted_at=unified_job.posted_date.isoformat() + "Z" if unified_job.posted_date else None,
        updated_at=None,
        source_rating=source_rating,
        provenance=provenance,
        score=unified_job.ai_score
    )

# Job search endpoints
@router.post("/jobs/search", response_model=SearchResponse)
async def search_jobs(
    request: SearchRequest,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Search for jobs across all enabled platforms using the standardized schema
    """
    try:
        start_time = time.time()
        request_id = f"req-{uuid.uuid4().hex[:6]}"
        
        # Convert search request to coordinator format
        query = " ".join(request.keywords) if request.keywords else "developer"
        category = None  # Not directly mapped in new schema
        
        # Get jobs from coordinator
        jobs = await coordinator.search_all_platforms(
            query=query,
            category=category,
            skills=request.skills,
            limit_per_platform=request.page_size
        )
        
        # Filter by requested sources if specified
        if request.sources:
            jobs = [job for job in jobs if job.platform in request.sources]
        
        # Convert to normalized format
        normalized_jobs = [_convert_unified_job_to_normalized(job) for job in jobs]
        
        # Apply sorting
        if request.sort_by == "recent":
            normalized_jobs.sort(key=lambda x: x.posted_at or "", reverse=True)
        elif request.sort_by == "budget_desc":
            normalized_jobs.sort(key=lambda x: x.budget_max or 0, reverse=True)
        elif request.sort_by == "budget_asc":
            normalized_jobs.sort(key=lambda x: x.budget_min or 0)
        else:  # relevance
            normalized_jobs.sort(key=lambda x: x.score or 0, reverse=True)
        
        # Apply top_k limit
        if request.top_k:
            normalized_jobs = normalized_jobs[:request.top_k]
        
        # Apply page_size limit
        if request.page_size:
            normalized_jobs = normalized_jobs[:request.page_size]
        
        # Calculate execution time
        took_ms = int((time.time() - start_time) * 1000)
        
        # Create metadata
        meta = SearchResponseMeta(
            request_id=request_id,
            sources_hit=list(set(job.source for job in normalized_jobs)),
            took_ms=took_ms,
            limits={"rate_limited_sources": []}  # Would be populated by actual rate limiting
        )
        
        return SearchResponse(
            jobs=normalized_jobs,
            next_cursor=None,  # Would implement proper pagination
            meta=meta
        )
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to search jobs")

# Legacy endpoint for backward compatibility
@router.post("/jobs/search/legacy", response_model=List[JobResponse])
async def search_jobs_legacy(
    request: JobSearchRequest,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Legacy job search endpoint (deprecated)
    """
    try:
        jobs = await coordinator.search_all_platforms(
            query=request.query,
            category=request.category,
            skills=request.skills,
            limit_per_platform=request.limit_per_platform
        )
        
        # Filter by requested platforms if specified
        if request.platforms:
            jobs = [job for job in jobs if job.platform in request.platforms]
        
        return jobs
        
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to search jobs")

@router.get("/jobs/{job_id}", response_model=Job)
async def get_job_details(
    job_id: str,
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get detailed information for a specific job in normalized format
    """
    try:
        job = await coordinator.get_job_details(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return _convert_unified_job_to_normalized(job)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job details: {e}")
        raise HTTPException(status_code=500, detail="Failed to get job details")

@router.get("/jobs/trending", response_model=List[Job])
async def get_trending_jobs(
    category: Optional[str] = Query(None, description="Category filter"),
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get trending jobs across platforms in normalized format
    """
    try:
        jobs = await coordinator.get_trending_jobs(category)
        return [_convert_unified_job_to_normalized(job) for job in jobs]
        
    except Exception as e:
        logger.error(f"Error getting trending jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trending jobs")

# User management endpoints
@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: str = Depends(get_current_user),
    identity_manager: IdentityManager = Depends(get_identity_manager)
):
    """
    Get current user's profile
    """
    try:
        profile = await identity_manager.get_user_profile(current_user)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to get user profile")

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_data: UserProfile,
    current_user: str = Depends(get_current_user),
    identity_manager: IdentityManager = Depends(get_identity_manager)
):
    """
    Update user profile
    """
    try:
        updated_profile = await identity_manager.update_user_profile(
            current_user, profile_data.dict()
        )
        return updated_profile
        
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

# Proposal management
@router.post("/proposals")
async def submit_proposal(
    request: ProposalRequest,
    current_user: str = Depends(get_current_user),
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Submit a proposal for a job
    """
    try:
        success = await coordinator.submit_proposal(
            request.job_id, request.dict()
        )
        
        if success:
            return {"message": "Proposal submitted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to submit proposal")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting proposal: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit proposal")

# Platform management
@router.get("/platforms/status")
async def get_platforms_status(
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get status of all platforms
    """
    try:
        return coordinator.get_status()
        
    except Exception as e:
        logger.error(f"Error getting platform status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get platform status")

@router.get("/platforms/categories")
async def get_platform_categories(
    platform: str = Query(..., description="Platform name (upwork or fiverr)"),
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get available categories for a platform
    """
    try:
        if platform == "fiverr" and coordinator.fiverr_agent:
            categories = await coordinator.fiverr_agent.get_categories()
            return {"platform": platform, "categories": categories}
        elif platform == "upwork":
            # Upwork categories would be hardcoded or fetched differently
            return {"platform": platform, "categories": []}
        else:
            raise HTTPException(status_code=400, detail="Platform not supported")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting platform categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to get categories")

# Analytics endpoints
@router.get("/analytics/job-trends")
async def get_job_trends(
    category: Optional[str] = Query(None, description="Category filter"),
    days: int = Query(7, description="Number of days to analyze"),
    coordinator: Coordinator = Depends(get_coordinator)
):
    """
    Get job posting trends and analytics
    """
    try:
        # This would implement analytics logic
        # For now, return placeholder data
        return {
            "category": category,
            "period_days": days,
            "total_jobs": 0,
            "platform_breakdown": {
                "upwork": 0,
                "fiverr": 0
            },
            "trends": []
        }
        
    except Exception as e:
        logger.error(f"Error getting job trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

# Health and monitoring
@router.get("/health/detailed")
async def detailed_health_check(
    coordinator: Coordinator = Depends(get_coordinator),
    identity_manager: IdentityManager = Depends(get_identity_manager)
):
    """
    Detailed health check for all services
    """
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "coordinator": coordinator.get_status(),
            "identity_manager": {
                "status": "operational",
                "user_count": await identity_manager.get_user_count()
            }
        }
        
    except Exception as e:
        logger.error(f"Error in detailed health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        } 