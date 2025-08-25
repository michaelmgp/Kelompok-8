import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import aiohttp
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity

logger = logging.getLogger(__name__)

@dataclass
class UpworkJob:
    id: str
    title: str
    description: str
    budget: Optional[str]
    skills: List[str]
    client_info: Dict[str, Any]
    posted_date: datetime
    url: str
    ai_score: Optional[float] = None

class UpworkAgent:
    """
    Fetch.ai agent for Upwork job scraping and analysis
    """
    
    def __init__(self, api_key: str, entity: Entity):
        self.api_key = api_key
        self.entity = entity
        self.ledger_api = LedgerApi("https://rest.fetch.ai")
        self.session = None
        self.base_url = "https://www.upwork.com/api/v2"
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "JobPlatformBot/1.0"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_jobs(
        self, 
        query: str, 
        category: str = None,
        skills: List[str] = None,
        limit: int = 50
    ) -> List[UpworkJob]:
        """
        Search for jobs on Upwork based on criteria
        """
        try:
            params = {
                "q": query,
                "limit": limit,
                "paging": 0
            }
            
            if category:
                params["subcategory2"] = category
                
            async with self.session.get(
                f"{self.base_url}/search/jobs",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    jobs = []
                    
                    for job_data in data.get("jobs", []):
                        job = self._parse_job_data(job_data)
                        if job:
                            # Apply AI scoring
                            job.ai_score = await self._calculate_ai_score(job)
                            jobs.append(job)
                    
                    logger.info(f"Found {len(jobs)} jobs for query: {query}")
                    return jobs
                else:
                    logger.error(f"Failed to fetch jobs: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching Upwork jobs: {e}")
            return []
    
    def _parse_job_data(self, job_data: Dict[str, Any]) -> Optional[UpworkJob]:
        """
        Parse raw job data into UpworkJob object
        """
        try:
            return UpworkJob(
                id=job_data.get("id"),
                title=job_data.get("title", ""),
                description=job_data.get("snippet", ""),
                budget=job_data.get("budget", {}).get("amount"),
                skills=job_data.get("skills", []),
                client_info={
                    "country": job_data.get("client", {}).get("country"),
                    "total_spent": job_data.get("client", {}).get("total_spent"),
                    "hire_rate": job_data.get("client", {}).get("hire_rate")
                },
                posted_date=datetime.fromisoformat(
                    job_data.get("date_created", "").replace("Z", "+00:00")
                ),
                url=f"https://www.upwork.com/jobs/{job_data.get('id')}"
            )
        except Exception as e:
            logger.error(f"Error parsing job data: {e}")
            return None
    
    async def _calculate_ai_score(self, job: UpworkJob) -> float:
        """
        Calculate AI-powered relevance score for a job
        """
        try:
            # This would integrate with your AI model
            # For now, return a simple heuristic score
            score = 0.0
            
            # Budget scoring
            if job.budget:
                try:
                    budget_amount = float(job.budget.replace("$", "").replace(",", ""))
                    if budget_amount > 1000:
                        score += 0.3
                    elif budget_amount > 500:
                        score += 0.2
                    elif budget_amount > 100:
                        score += 0.1
                except:
                    pass
            
            # Skills scoring
            if job.skills:
                score += min(len(job.skills) * 0.05, 0.2)
            
            # Client reputation scoring
            if job.client_info.get("total_spent"):
                try:
                    total_spent = float(job.client_info["total_spent"])
                    if total_spent > 10000:
                        score += 0.2
                    elif total_spent > 5000:
                        score += 0.1
                except:
                    pass
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating AI score: {e}")
            return 0.0
    
    async def get_job_details(self, job_id: str) -> Optional[UpworkJob]:
        """
        Get detailed information for a specific job
        """
        try:
            async with self.session.get(
                f"{self.base_url}/jobs/{job_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_job_data(data)
                else:
                    logger.error(f"Failed to fetch job details: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching job details: {e}")
            return None
    
    async def submit_proposal(self, job_id: str, proposal_data: Dict[str, Any]) -> bool:
        """
        Submit a proposal for a job (requires proper authentication)
        """
        try:
            # This would require proper Upwork API authentication
            # and proposal submission endpoints
            logger.info(f"Submitting proposal for job {job_id}")
            return True
        except Exception as e:
            logger.error(f"Error submitting proposal: {e}")
            return False 