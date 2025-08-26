"""
Job data models for the Explorer Agent

Defines the structure of job data throughout the system
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class JobLocation(BaseModel):
    """Job location information"""
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    remote: bool = False
    hybrid: bool = False
    onsite: bool = True

class JobRequirements(BaseModel):
    """Job requirements and qualifications"""
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    education: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)

class JobSalary(BaseModel):
    """Job salary information"""
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: str = "USD"
    period: str = "yearly"  # yearly, monthly, hourly
    benefits: List[str] = Field(default_factory=list)

class JobMetadata(BaseModel):
    """Job metadata and processing information"""
    source: str
    scraped_at: datetime
    processed_at: Optional[datetime] = None
    processing_version: str = "1.0.0"
    confidence_score: Optional[float] = None
    ai_analysis: Optional[Dict[str, Any]] = None

class JobListing(BaseModel):
    """Complete job listing information"""
    id: str
    title: str
    company: str
    location: JobLocation
    description: str
    requirements: JobRequirements
    salary: Optional[JobSalary] = None
    job_type: str = "Full-time"  # Full-time, Part-time, Contract, Internship
    experience_level: str = "Mid-level"  # Entry, Junior, Mid-level, Senior, Lead
    posted_date: Optional[datetime] = None
    application_deadline: Optional[datetime] = None
    application_url: Optional[str] = None
    company_website: Optional[str] = None
    industry: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: JobMetadata

class JobSearchQuery(BaseModel):
    """Job search query parameters"""
    keywords: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[str] = None
    job_type: Optional[str] = None
    industry: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    remote_only: bool = False
    limit: int = 50
    page: int = 1
    sort_by: str = "relevance"  # relevance, date, salary
    sort_order: str = "desc"  # asc, desc

class JobSearchResult(BaseModel):
    """Job search result with pagination"""
    jobs: List[JobListing]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    search_query: JobSearchQuery
    search_timestamp: datetime
    sources_searched: List[str]

class JobAnalysis(BaseModel):
    """AI-powered job analysis results"""
    job_id: str
    skill_match_score: float = Field(ge=0.0, le=1.0)
    experience_level_match: str
    company_reputation: Optional[str] = None
    salary_range_estimate: Optional[str] = None
    market_demand: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    analysis_timestamp: datetime
    ai_model_used: str

class JobStreamMessage(BaseModel):
    """WebSocket message for job streaming"""
    type: str  # job_data, status_update, scraper_status, error
    timestamp: datetime
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    scraper: Optional[str] = None
    status: Optional[str] = None
    error: Optional[str] = None

