import asyncio
import logging
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import json
from fetchai.ledger.crypto import Entity
from fetchai.ledger.contract import Contract

from .upwork_agent import UpworkAgent, UpworkJob
from .fiverr_agent import FiverrAgent, FiverrJob

logger = logging.getLogger(__name__)

@dataclass
class UnifiedJob:
    """Unified job representation across platforms"""
    id: str
    platform: str  # 'upwork' or 'fiverr'
    title: str
    description: str
    budget: Optional[str]
    skills: List[str]
    category: str
    posted_date: datetime
    url: str
    ai_score: float
    platform_specific_data: Dict[str, Any]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

class Coordinator:
    """
    Multi-platform coordinator for job aggregation and analysis
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.upwork_agent = None
        self.fiverr_agent = None
        self.entity = None
        self.contract = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the coordinator and all agents"""
        try:
            # Initialize Fetch.ai entity
            self.entity = Entity()
            
            # Initialize platform agents
            if self.config.get("upwork", {}).get("enabled", False):
                upwork_config = self.config["upwork"]
                self.upwork_agent = UpworkAgent(
                    api_key=upwork_config["api_key"],
                    entity=self.entity
                )
                await self.upwork_agent.__aenter__()
                logger.info("Upwork agent initialized")
            
            if self.config.get("fiverr", {}).get("enabled", False):
                fiverr_config = self.config["fiverr"]
                self.fiverr_agent = FiverrAgent(
                    api_key=fiverr_config["api_key"],
                    entity=self.entity
                )
                await self.fiverr_agent.__aenter__()
                logger.info("Fiverr agent initialized")
            
            # Initialize blockchain contract if configured
            if self.config.get("blockchain", {}).get("enabled", False):
                await self._initialize_blockchain()
            
            self.is_initialized = True
            logger.info("Coordinator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize coordinator: {e}")
            raise
    
    async def _initialize_blockchain(self):
        """Initialize blockchain integration"""
        try:
            # This would connect to your ICP blockchain
            # For now, just log the intention
            logger.info("Blockchain integration would be initialized here")
        except Exception as e:
            logger.error(f"Failed to initialize blockchain: {e}")
    
    async def search_all_platforms(
        self,
        query: str,
        category: str = None,
        skills: List[str] = None,
        limit_per_platform: int = 25
    ) -> List[UnifiedJob]:
        """
        Search for jobs across all enabled platforms
        """
        if not self.is_initialized:
            raise RuntimeError("Coordinator not initialized")
        
        tasks = []
        
        # Add Upwork search task
        if self.upwork_agent:
            tasks.append(
                self._search_upwork(query, category, skills, limit_per_platform)
            )
        
        # Add Fiverr search task
        if self.fiverr_agent:
            tasks.append(
                self._search_fiverr(query, category, skills, limit_per_platform)
            )
        
        # Execute all searches concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine and process results
        all_jobs = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Search task failed: {result}")
            else:
                all_jobs.extend(result)
        
        # Sort by AI score and return
        all_jobs.sort(key=lambda x: x.ai_score, reverse=True)
        return all_jobs
    
    async def _search_upwork(
        self,
        query: str,
        category: str = None,
        skills: List[str] = None,
        limit: int = 25
    ) -> List[UnifiedJob]:
        """Search Upwork and convert to unified format"""
        try:
            upwork_jobs = await self.upwork_agent.search_jobs(
                query, category, skills, limit
            )
            
            unified_jobs = []
            for job in upwork_jobs:
                # Generate normalized ID: upwork:<source_id>
                normalized_id = f"upwork:{job.id}"
                
                unified_job = UnifiedJob(
                    id=normalized_id,
                    platform="upwork",
                    title=job.title,
                    description=job.description,
                    budget=job.budget,
                    skills=job.skills,
                    category="",  # Upwork doesn't have direct category
                    posted_date=job.posted_date,
                    url=job.url,
                    ai_score=job.ai_score or 0.0,
                    platform_specific_data={
                        "client_info": job.client_info,
                        "original_id": job.id,
                        "source_id": job.id
                    }
                )
                unified_jobs.append(unified_job)
            
            return unified_jobs
            
        except Exception as e:
            logger.error(f"Error searching Upwork: {e}")
            return []
    
    async def _search_fiverr(
        self,
        query: str,
        category: str = None,
        skills: List[str] = None,
        limit: int = 25
    ) -> List[UnifiedJob]:
        """Search Fiverr and convert to unified format"""
        try:
            fiverr_jobs = await self.fiverr_agent.search_gigs(
                query, category, None, limit
            )
            
            unified_jobs = []
            for job in fiverr_jobs:
                # Generate normalized ID: fiverr:<source_id>
                normalized_id = f"fiverr:{job.id}"
                
                unified_job = UnifiedJob(
                    id=normalized_id,
                    platform="fiverr",
                    title=job.title,
                    description=job.description,
                    budget=job.price,
                    skills=skills or [],  # Fiverr doesn't have direct skills
                    category=job.category,
                    posted_date=datetime.utcnow(),  # Fiverr doesn't provide posting date
                    url=job.url,
                    ai_score=job.ai_score or 0.0,
                    platform_specific_data={
                        "seller_info": job.seller_info,
                        "rating": job.rating,
                        "review_count": job.review_count,
                        "delivery_time": job.delivery_time,
                        "original_id": job.id,
                        "source_id": job.id
                    }
                )
                unified_jobs.append(unified_job)
            
            return unified_jobs
            
        except Exception as e:
            logger.error(f"Error searching Fiverr: {e}")
            return []
    
    async def get_job_details(self, job_id: str) -> Optional[UnifiedJob]:
        """Get detailed information for a specific job"""
        if not self.is_initialized:
            raise RuntimeError("Coordinator not initialized")
        
        try:
            if job_id.startswith("upwork:"):
                if not self.upwork_agent:
                    return None
                original_id = job_id.replace("upwork:", "")
                upwork_job = await self.upwork_agent.get_job_details(original_id)
                if upwork_job:
                    return UnifiedJob(
                        id=job_id,
                        platform="upwork",
                        title=upwork_job.title,
                        description=upwork_job.description,
                        budget=upwork_job.budget,
                        skills=upwork_job.skills,
                        category="",
                        posted_date=upwork_job.posted_date,
                        url=upwork_job.url,
                        ai_score=upwork_job.ai_score or 0.0,
                        platform_specific_data={
                            "client_info": upwork_job.client_info,
                            "original_id": upwork_job.id,
                            "source_id": upwork_job.id
                        }
                    )
            
            elif job_id.startswith("fiverr:"):
                if not self.fiverr_agent:
                    return None
                original_id = job_id.replace("fiverr:", "")
                fiverr_job = await self.fiverr_agent.get_gig_details(original_id)
                if fiverr_job:
                    return UnifiedJob(
                        id=job_id,
                        platform="fiverr",
                        title=fiverr_job.title,
                        description=fiverr_job.description,
                        budget=fiverr_job.price,
                        skills=[],
                        category=fiverr_job.category,
                        posted_date=datetime.utcnow(),
                        url=fiverr_job.url,
                        ai_score=fiverr_job.ai_score or 0.0,
                        platform_specific_data={
                            "seller_info": fiverr_job.seller_info,
                            "rating": fiverr_job.rating,
                            "review_count": fiverr_job.review_count,
                            "delivery_time": fiverr_job.delivery_time,
                            "original_id": fiverr_job.id,
                            "source_id": fiverr_job.id
                        }
                    )
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting job details: {e}")
            return None
    
    async def get_trending_jobs(self, category: str = None) -> List[UnifiedJob]:
        """Get trending jobs across platforms"""
        if not self.is_initialized:
            raise RuntimeError("Coordinator not initialized")
        
        tasks = []
        
        if self.fiverr_agent:
            tasks.append(self.fiverr_agent.get_trending_gigs(category))
        
        # Note: Upwork doesn't have a trending jobs endpoint
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_jobs = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Trending search failed: {result}")
            else:
                # Convert Fiverr gigs to unified format
                for gig in result:
                    # Generate normalized ID: fiverr:<source_id>
                    normalized_id = f"fiverr:{gig.id}"
                    
                    unified_job = UnifiedJob(
                        id=normalized_id,
                        platform="fiverr",
                        title=gig.title,
                        description=gig.description,
                        budget=gig.price,
                        skills=[],
                        category=gig.category,
                        posted_date=datetime.utcnow(),
                        url=gig.url,
                        ai_score=gig.ai_score or 0.0,
                        platform_specific_data={
                            "seller_info": gig.seller_info,
                            "rating": gig.rating,
                            "review_count": gig.review_count,
                            "delivery_time": gig.delivery_time,
                            "original_id": gig.id,
                            "source_id": gig.id
                        }
                    )
                    all_jobs.append(unified_job)
        
        all_jobs.sort(key=lambda x: x.ai_score, reverse=True)
        return all_jobs
    
    async def submit_proposal(self, job_id: str, proposal_data: Dict[str, Any]) -> bool:
        """Submit a proposal for a job"""
        if not self.is_initialized:
            raise RuntimeError("Coordinator not initialized")
        
        try:
            if job_id.startswith("upwork:"):
                if not self.upwork_agent:
                    return False
                original_id = job_id.replace("upwork:", "")
                return await self.upwork_agent.submit_proposal(original_id, proposal_data)
            
            # Fiverr doesn't support proposal submission through API
            logger.warning("Proposal submission not supported for Fiverr")
            return False
            
        except Exception as e:
            logger.error(f"Error submitting proposal: {e}")
            return False
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            if self.upwork_agent:
                await self.upwork_agent.__aexit__(None, None, None)
            
            if self.fiverr_agent:
                await self.fiverr_agent.__aexit__(None, None, None)
                
            logger.info("Coordinator cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during coordinator cleanup: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get coordinator status"""
        return {
            "initialized": self.is_initialized,
            "upwork_enabled": self.upwork_agent is not None,
            "fiverr_enabled": self.fiverr_agent is not None,
            "blockchain_enabled": self.contract is not None
        } 