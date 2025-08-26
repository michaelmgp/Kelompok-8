"""
Base scraper class for job websites

Defines the interface that all job scrapers must implement
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, AsyncGenerator, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Abstract base class for all job scrapers"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.base_url = ""
        self.session = None
        self.is_initialized = False
        
    @abstractmethod
    async def initialize(self):
        """Initialize the scraper (setup session, headers, etc.)"""
        pass
        
    @abstractmethod
    async def scrape_jobs(self, search_params: Optional[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Scrape jobs and yield them one by one"""
        pass
        
    @abstractmethod
    async def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """Get detailed information for a specific job"""
        pass
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
            
    def _validate_search_params(self, search_params: Optional[Dict] = None) -> Dict[str, Any]:
        """Validate and set default search parameters"""
        if not search_params:
            search_params = {}
            
        defaults = {
            "keywords": "",
            "location": "",
            "experience_level": "",
            "job_type": "",
            "limit": 50,
            "page": 1
        }
        
        # Merge with defaults
        for key, default_value in defaults.items():
            if key not in search_params:
                search_params[key] = default_value
                
        return search_params
        
    def _is_valid_job_data(self, raw_data: Dict[str, Any]) -> bool:
        """Basic validation to catch obviously invalid job data early"""
        try:
            # Safety check for None or invalid raw_data
            if not raw_data or not isinstance(raw_data, dict):
                logger.debug(f"Cannot validate invalid raw_data: {type(raw_data)}")
                return False
                
            # Check for required fields
            title = raw_data.get("title", "").strip()
            company = raw_data.get("company", "").strip()
            description = raw_data.get("description", "").strip()
            
            # Reject jobs with missing essential fields
            if not title or not company:
                logger.debug(f"Rejecting job: Missing title or company")
                return False
                
            # Reject jobs with very short descriptions
            if len(description) < 10:  # Reduced from 20 to 10
                logger.debug(f"Rejecting job: Description too short ({len(description)} chars)")
                return False
                
            # Reject jobs with obvious placeholder content
            if any(placeholder in title.lower() for placeholder in ["test", "sample", "example", "placeholder"]):
                logger.debug(f"Rejecting job: Placeholder title detected")
                return False
                
            # Only reject if title is completely empty, not just short
            if len(title) < 3:  # Reduced from 5 to 3
                logger.debug(f"Rejecting job: Title too short")
                return False
                
            # Reject jobs with obvious error messages
            error_indicators = ["error", "not found", "access denied", "forbidden", "unauthorized"]
            if any(error in description.lower() for error in error_indicators):
                logger.debug(f"Rejecting job: Error content detected")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error validating job data: {e}")
            return False
        
    def _create_job_object(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a standardized job object that matches the frontend structure exactly"""
        # Safety check for None or invalid raw_data
        if not raw_data or not isinstance(raw_data, dict):
            logger.debug(f"Cannot create job object from invalid raw_data: {type(raw_data)}")
            return None
            
        # Basic validation is disabled for now - accept all jobs
        # if not self._is_valid_job_data(raw_data):
        #     return None
            
        return {
            "id": raw_data.get("id", str(hash(raw_data.get("title", "")))),  # Ensure unique ID
            "title": raw_data.get("title", ""),
            "company": raw_data.get("company", ""),
            "description": raw_data.get("description", ""),
            "jobDescription": raw_data.get("description", ""),  # Match frontend field
            "jobRequirements": raw_data.get("requirements", []),  # Match frontend field
            "salary": raw_data.get("salary", "Not specified"),
            "skills": raw_data.get("extracted_skills", []),  # Match frontend field
            "rating": 4.5,  # Default rating like frontend
            "location": raw_data.get("location", ""),
            "postedDate": raw_data.get("posted_date", "Recently"),
            # Additional fields for explorer agent
            "source": self.name,
            "scraped_at": datetime.now().isoformat(),
            "application_url": raw_data.get("application_url", ""),
            "original_url": raw_data.get("original_url", ""),  # Original job posting URL
            "full_description": raw_data.get("full_description", ""),  # Complete job description
            "job_type": raw_data.get("job_type", "Full-time"),
            "experience_level": raw_data.get("experience_level", "Mid-level"),
            "raw_data": raw_data
        }
        
    async def _make_request(self, url: str, method: str = "GET", **kwargs) -> Optional[Any]:
        """Make HTTP request with error handling and retries"""
        if not self.is_initialized:
            await self.initialize()
            
        try:
            # Implementation depends on the HTTP client being used
            # This is a placeholder for the actual implementation
            pass
        except Exception as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
            
    def _extract_text(self, element) -> str:
        """Extract text from HTML element safely"""
        if element is None:
            return ""
        return element.get_text(strip=True) if hasattr(element, 'get_text') else str(element)
        
    def _extract_attribute(self, element, attribute: str, default: str = "") -> str:
        """Extract attribute from HTML element safely"""
        if element is None:
            return default
        return element.get(attribute, default) if hasattr(element, 'get') else default
