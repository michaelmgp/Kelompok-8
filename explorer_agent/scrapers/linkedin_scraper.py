"""
LinkedIn job scraper

Scrapes job listings from LinkedIn Jobs
"""

import asyncio
import logging
from typing import Dict, List, Optional, AsyncGenerator, Any
import aiohttp
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class LinkedInScraper(BaseScraper):
    """LinkedIn Jobs scraper"""
    
    def __init__(self):
        super().__init__()
        self.name = "LinkedIn"
        self.base_url = "https://www.linkedin.com/jobs"
        self.session = None
        
    async def initialize(self):
        """Initialize the LinkedIn scraper"""
        if self.is_initialized:
            return
            
        # Create aiohttp session with headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        
        self.session = aiohttp.ClientSession(headers=headers)
        self.is_initialized = True
        logger.info("LinkedIn scraper initialized")
        
    async def scrape_jobs(self, search_params: Optional[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Scrape jobs from LinkedIn based on search parameters"""
        if not self.is_initialized:
            await self.initialize()
            
        search_params = self._validate_search_params(search_params)
        
        try:
            # Build search URL
            search_url = self._build_search_url(search_params)
            logger.info(f"Searching LinkedIn jobs: {search_url}")
            
            # Get search results page
            html_content = await self._make_request(search_url)
            if not html_content:
                logger.error("Failed to get LinkedIn search results")
                return
                
            # Parse job listings
            job_listings = await self._parse_job_listings(html_content)
            
            # Yield each job
            for job_data in job_listings:
                yield self._create_job_object(job_data)
                
                # Rate limiting
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error scraping LinkedIn jobs: {e}")
            
    async def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """Get detailed information for a specific LinkedIn job"""
        if not self.is_initialized:
            await self.initialize()
            
        try:
            html_content = await self._make_request(job_url)
            if not html_content:
                return {}
                
            # Parse detailed job information
            job_details = await self._parse_job_details(html_content)
            return self._create_job_object(job_details)
            
        except Exception as e:
            logger.error(f"Error getting LinkedIn job details: {e}")
            return {}
            
    def _build_search_url(self, search_params: Dict[str, Any]) -> str:
        """Build LinkedIn search URL from parameters"""
        base = f"{self.base_url}/search"
        params = []
        
        if search_params.get("keywords"):
            params.append(f"keywords={search_params['keywords']}")
            
        if search_params.get("location"):
            params.append(f"location={search_params['location']}")
            
        if search_params.get("experience_level"):
            params.append(f"experience={search_params['experience_level']}")
            
        if search_params.get("job_type"):
            params.append(f"jobType={search_params['job_type']}")
            
        if search_params.get("page") and search_params["page"] > 1:
            params.append(f"start={search_params['page'] * 25}")
            
        if params:
            return f"{base}?{'&'.join(params)}"
        return base
        
    async def _make_request(self, url: str) -> Optional[str]:
        """Make HTTP request to LinkedIn"""
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"LinkedIn request failed with status {response.status}")
                    return None
        except Exception as e:
            logger.error(f"LinkedIn request error: {e}")
            return None
            
    async def _parse_job_listings(self, html_content: str) -> List[Dict[str, Any]]:
        """Parse job listings from LinkedIn HTML"""
        jobs = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find job cards (this selector may need updates based on LinkedIn's current structure)
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards:
                try:
                    job_data = self._extract_job_from_card(card)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.debug(f"Error parsing job card: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing LinkedIn job listings: {e}")
            
        return jobs
        
    def _extract_job_from_card(self, card) -> Optional[Dict[str, Any]]:
        """Extract job information from a single job card"""
        try:
            # Extract job title
            title_elem = card.find('h3', class_='base-search-card__title')
            title = self._extract_text(title_elem)
            
            # Extract company name
            company_elem = card.find('h4', class_='base-search-card__subtitle')
            company = self._extract_text(company_elem)
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location')
            location = self._extract_text(location_elem)
            
            # Extract job URL
            link_elem = card.find('a', class_='base-card__full-link')
            job_url = self._extract_attribute(link_elem, 'href', '')
            
            # Extract posted date
            date_elem = card.find('time')
            posted_date = self._extract_attribute(date_elem, 'datetime', '')
            
            # Additional validation for LinkedIn-specific issues
            if not title or not company or not job_url:
                logger.debug(f"Rejecting LinkedIn job: Missing essential data")
                return None
                
            # Check for obvious placeholder or error content
            if any(placeholder in title.lower() for placeholder in ["test", "sample", "example", "placeholder", "error"]):
                logger.debug(f"Rejecting LinkedIn job: Placeholder title detected")
                return None
                
            # Check for very short titles (likely incomplete)
            if len(title) < 5:
                logger.debug(f"Rejecting LinkedIn job: Title too short")
                return None
                
            return {
                "id": job_url.split('/')[-1] if job_url else "",
                "title": title,
                "company": company,
                "location": location,
                "description": "",  # Will be filled in get_job_details
                "requirements": [],
                "salary": "",
                "job_type": "Full-time",
                "experience_level": "Mid-level",
                "posted_date": posted_date,
                "application_url": job_url,
                "original_url": job_url,  # Original LinkedIn job posting URL
                "full_description": "",  # Will be filled in get_job_details
                "extracted_skills": [],  # Will be populated by processor
                "raw_data": {
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": job_url
                }
            }
            
        except Exception as e:
            logger.debug(f"Error extracting job from card: {e}")
            return None
            
    async def _parse_job_details(self, html_content: str) -> Dict[str, Any]:
        """Parse detailed job information from LinkedIn job page"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract job description
            description_elem = soup.find('div', class_='show-more-less-html')
            description = self._extract_text(description_elem)
            
            # Extract requirements (this is a simplified approach)
            requirements = []
            requirements_elem = soup.find('div', class_='description__text')
            if requirements_elem:
                # Look for common requirement patterns
                text = self._extract_text(requirements_elem)
                # Simple keyword-based requirement extraction
                requirement_keywords = ['experience', 'skills', 'requirements', 'qualifications']
                for keyword in requirement_keywords:
                    if keyword in text.lower():
                        requirements.append(f"See {keyword} in description")
                        break
                        
            # Validate job description quality
            if not description or len(description.strip()) < 50:
                logger.debug(f"Rejecting LinkedIn job: Description too short or empty")
                return {}
                
            # Check for error messages or blocked content
            error_indicators = ["access denied", "content blocked", "page not available", "error occurred"]
            if any(error in description.lower() for error in error_indicators):
                logger.debug(f"Rejecting LinkedIn job: Error content in description")
                return {}
                
            return {
                "description": description,
                "full_description": description,  # Store the complete description
                "requirements": requirements,
                "salary": "",  # LinkedIn typically doesn't show salary in job descriptions
                "job_type": "",
                "experience_level": ""
            }
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn job details: {e}")
            return {}
            
    async def cleanup(self):
        """Cleanup LinkedIn scraper resources"""
        if self.session:
            await self.session.close()
        self.is_initialized = False
        logger.info("LinkedIn scraper cleaned up")

