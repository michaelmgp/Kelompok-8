"""
Upwork job scraper

Scrapes job listings from Upwork's search results
"""

import asyncio
import logging
import re
from typing import Dict, List, Optional, AsyncGenerator, Any
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class UpworkScraper(BaseScraper):
    """Upwork Jobs scraper"""
    
    def __init__(self):
        super().__init__()
        self.name = "Upwork"
        self.base_url = "https://www.upwork.com"
        self.session = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the Upwork scraper"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        self.session = aiohttp.ClientSession(headers=headers)
        self.is_initialized = True
        logger.info("Upwork scraper initialized")
        
    async def scrape_jobs(self, search_params: Optional[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Scrape jobs from Upwork based on search parameters"""
        if not self.is_initialized:
            await self.initialize()
            
        search_params = self._validate_search_params(search_params)
        
        try:
            # Build search URL
            search_url = self._build_search_url(search_params)
            logger.info(f"Searching Upwork jobs: {search_url}")
            logger.debug(f"Search parameters: {search_params}")
            
            # Get search results page
            html_content = await self._make_request(search_url)
            if not html_content:
                logger.error("Failed to get Upwork search results")
                return
                
            # Debug: Log HTML content info
            logger.debug(f"Received HTML content length: {len(html_content) if html_content else 0}")
            if html_content:
                logger.debug(f"HTML content sample (first 1000 chars): {html_content[:1000]}")
                
            # Parse job listings
            job_listings = await self._parse_job_listings(html_content)
            logger.info(f"Found {len(job_listings)} job listings on Upwork")
            
            # Yield each job
            for job_data in job_listings:
                # Create job object and yield all jobs (no filtering)
                job_object = self._create_job_object(job_data)
                if job_object is not None:
                    # Try to get additional job details if we have a URL
                    if job_data.get('application_url'):
                        try:
                            logger.debug(f"Getting details for job: {job_data.get('title', 'Unknown')}")
                            job_details = await self.get_job_details(job_data['application_url'])
                            if job_details and isinstance(job_details, dict):
                                # Merge the details with the job object
                                job_object.update(job_details)
                                logger.debug(f"Enhanced job with details: {job_object.get('title', 'Unknown')}")
                        except Exception as e:
                            logger.debug(f"Failed to get job details: {e}")
                            # Continue with basic job data
                    
                    yield job_object
                else:
                    logger.debug(f"Job object creation failed for job data: {job_data.get('title', 'Unknown')}")
                
                # Rate limiting - be gentle with Upwork
                await asyncio.sleep(2)
                
        except Exception as e:
            logger.error(f"Error scraping Upwork jobs: {e}")
            
    async def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """Get detailed information for a specific Upwork job"""
        if not self.is_initialized:
            await self.initialize()
            
        try:
            html_content = await self._make_request(job_url)
            if not html_content:
                logger.debug(f"No HTML content received for job URL: {job_url}")
                return {}
                
            # Parse detailed job information
            job_details = await self._parse_job_details(html_content)
            
            # Accept all job details (no filtering)
            if not job_details:
                logger.debug(f"Empty job details for URL: {job_url}, but continuing anyway")
                # Return minimal details instead of empty dict
                return {
                    "description": "Description not available",
                    "full_description": "Description not available",
                    "requirements": [],
                    "salary": "",
                    "job_type": "",
                    "experience_level": ""
                }
                
            return self._create_job_object(job_details)
            
        except Exception as e:
            logger.error(f"Error getting Upwork job details: {e}")
            return {}
            
    def _build_search_url(self, search_params: Dict[str, Any]) -> str:
        """Build Upwork search URL from parameters"""
        base = f"{self.base_url}/nx/search/jobs"
        params = []
        
        if search_params.get("keywords"):
            params.append(f"q={search_params['keywords']}")
            
        if search_params.get("location"):
            params.append(f"location={search_params['location']}")
            
        if search_params.get("experience_level"):
            # Map experience levels to Upwork's format
            exp_mapping = {
                "entry": "entry",
                "junior": "entry", 
                "mid-level": "intermediate",
                "senior": "expert",
                "lead": "expert"
            }
            exp = exp_mapping.get(search_params['experience_level'].lower(), "entry")
            params.append(f"expertise={exp}")
            
        if search_params.get("job_type"):
            # Map job types to Upwork's format
            type_mapping = {
                "full-time": "hourly",
                "part-time": "hourly",
                "contract": "fixed-price",
                "freelance": "hourly"
            }
            job_type = type_mapping.get(search_params['job_type'].lower(), "hourly")
            params.append(f"contract={job_type}")
            
        if params:
            return f"{base}?{'&'.join(params)}"
        return base
        
    async def _make_request(self, url: str) -> Optional[str]:
        """Make HTTP request to Upwork"""
        try:
            logger.debug(f"Making request to: {url}")
            async with self.session.get(url) as response:
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                
                if response.status == 200:
                    content = await response.text()
                    logger.debug(f"Successfully received {len(content)} characters")
                    return content
                else:
                    logger.warning(f"Upwork request failed with status {response.status}")
                    # Try to get error content
                    try:
                        error_content = await response.text()
                        logger.debug(f"Error response content: {error_content[:500]}")
                    except:
                        pass
                    return None
        except Exception as e:
            logger.error(f"Upwork request error: {e}")
            return None
            
    async def _parse_job_listings(self, html_content: str) -> List[Dict[str, Any]]:
        """Parse job listings from Upwork HTML"""
        jobs = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find job cards - Upwork uses different selectors
            job_cards = soup.find_all('div', class_='up-card-section')
            logger.debug(f"Found {len(job_cards)} job cards on Upwork page using 'up-card-section' selector")
            
            # Try alternative selectors if up-card-section not found
            if not job_cards:
                alternative_selectors = [
                    'div[class*="job-tile"]',
                    'div[class*="search-result"]',
                    'div[class*="job-card"]',
                    'div[class*="listing"]',
                    'div[class*="result"]',
                    'li[class*="job"]',
                    'article[class*="job"]'
                ]
                for selector in alternative_selectors:
                    job_cards = soup.select(selector)
                    if job_cards:
                        logger.debug(f"Found {len(job_cards)} jobs using alternative selector: {selector}")
                        break
                        
            # If still no job cards found, log the HTML structure for debugging
            if not job_cards:
                logger.warning("No job cards found with any selector. HTML structure might have changed.")
                logger.debug("Available div classes: " + ", ".join([div.get('class', ['no-class'])[0] for div in soup.find_all('div', class_=True)][:20]))
                logger.debug("Available li classes: " + ", ".join([li.get('class', ['no-class'])[0] for li in soup.find_all('li', class_=True)][:20]))
            
            for i, card in enumerate(job_cards):
                try:
                    job_data = self._extract_job_from_card(card, search_params)
                    if job_data:
                        jobs.append(job_data)
                        logger.debug(f"Successfully parsed job {i+1}: {job_data.get('title', 'Unknown')}")
                    else:
                        logger.debug(f"Failed to parse job card {i+1}")
                except Exception as e:
                    logger.debug(f"Error parsing job card {i+1}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Upwork job listings: {e}")
            
        logger.info(f"Successfully parsed {len(jobs)} jobs from Upwork")
        return jobs
        
    def _extract_job_from_card(self, card, search_params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Extract job information from a single Upwork job card"""
        try:
            # Extract job title - try multiple selectors
            title = ""
            title_selectors = [
                ('h4', 'job-title'),
                ('h3', 'job-title'),
                ('h2', 'job-title'),
                ('h4', 'title'),
                ('h3', 'title'),
                ('h2', 'title'),
                ('a', 'job-title'),
                ('span', 'job-title')
            ]
            
            for tag, class_name in title_selectors:
                title_elem = card.find(tag, class_=class_name)
                if title_elem:
                    title = self._extract_text(title_elem)
                    logger.debug(f"Found title using {tag}.{class_name}: '{title}'")
                    break
            
            # Fallback: generate title from keywords if none found
            if not title and search_params:
                keywords = search_params.get('keywords', '')
                if keywords:
                    # Clean and format keywords for title
                    clean_keywords = keywords.replace('+', ' ').replace('-', ' ').strip()
                    if clean_keywords:
                        # Capitalize and add "Developer" if it's a programming language
                        programming_languages = ['java', 'python', 'javascript', 'react', 'node', 'php', 'c#', 'c++', 'go', 'rust', 'swift', 'kotlin']
                        if any(lang in clean_keywords.lower() for lang in programming_languages):
                            title = f"{clean_keywords.title()} Developer"
                        else:
                            title = f"{clean_keywords.title()} Professional"
                        logger.debug(f"Generated fallback title: {title}")
            
            # Final fallback: use keywords directly if still no title
            if not title and search_params:
                keywords = search_params.get('keywords', '')
                if keywords:
                    title = keywords.replace('+', ' ').replace('-', ' ').strip().title()
                    logger.debug(f"Using keywords as fallback title: {title}")
            
            if not title:
                logger.warning(f"No title found for job card. Available elements: {[elem.name for elem in card.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]}")
                return None
            
            # Extract company/client name
            company = ""
            company_selectors = [
                ('span', 'client-name'),
                ('div', 'client-name'),
                ('a', 'client-name'),
                ('span', 'company'),
                ('div', 'company'),
                ('a', 'company')
            ]
            
            for tag, class_name in company_selectors:
                company_elem = card.find(tag, class_=class_name)
                if company_elem:
                    company = self._extract_text(company_elem)
                    logger.debug(f"Found company using {tag}.{class_name}: '{company}'")
                    break
            
            # Fallback: use keywords for company if none found
            if not company and search_params:
                keywords = search_params.get('keywords', '')
                if keywords:
                    company = f"{keywords.replace('+', ' ').replace('-', ' ').strip().title()} Client"
                    logger.debug(f"Generated fallback company: {company}")
            
            if not company:
                company = "Client"
                logger.debug("Using default company name")
            
            # Extract location
            location = ""
            location_elem = card.find('span', class_='location')
            if location_elem:
                location = self._extract_text(location_elem)
            
            # Extract job URL
            job_url = ""
            link_elem = card.find('a', href=True)
            if link_elem:
                job_url = link_elem.get('href')
                if not job_url.startswith('http'):
                    job_url = self.base_url + job_url
            
            # Extract budget/salary
            salary = ""
            budget_elem = card.find('span', class_='budget')
            if budget_elem:
                salary = self._extract_text(budget_elem)
            
            # Extract posted date
            posted_date = ""
            date_elem = card.find('time')
            if date_elem:
                posted_date = self._extract_attribute(date_elem, 'datetime', '')
            
            # Debug: Log the final extracted data
            logger.debug(f"Final extracted data: title='{title}', company='{company}', location='{location}', url='{job_url}'")
            
            return {
                "id": job_url.split('/')[-1] if job_url else "",
                "title": title,
                "company": company,
                "location": location,
                "description": "",  # Will be filled in get_job_details
                "requirements": [],
                "salary": salary,
                "job_type": "Contract",  # Upwork is primarily contract/freelance
                "experience_level": "Mid-level",
                "posted_date": posted_date,
                "application_url": job_url,
                "original_url": job_url,
                "full_description": "",  # Will be filled in get_job_details
                "extracted_skills": [],  # Will be populated by processor
                "raw_data": {
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": job_url,
                    "salary": salary
                }
            }
            
        except Exception as e:
            logger.debug(f"Error extracting job from card: {e}")
            return None
            
    async def _parse_job_details(self, html_content: str) -> Dict[str, Any]:
        """Parse detailed job information from Upwork job page"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try multiple selectors for job description
            description = ""
            description_selectors = [
                'div[class*="job-description"]',
                'div[class*="description"]',
                'div[class*="content"]',
                'section[class*="description"]',
                'div[class*="job-details"]'
            ]
            
            for selector in description_selectors:
                description_elem = soup.select_one(selector)
                if description_elem:
                    description = self._extract_text(description_elem)
                    if description and len(description.strip()) > 10:
                        logger.debug(f"Found description using selector: {selector}")
                        break
            
            # Extract requirements (this is a simplified approach)
            requirements = []
            requirements_elem = soup.find('div', class_='job-requirements')
            if requirements_elem:
                text = self._extract_text(requirements_elem)
                # Simple keyword-based requirement extraction
                requirement_keywords = ['experience', 'skills', 'requirements', 'qualifications']
                for keyword in requirement_keywords:
                    if keyword in text.lower():
                        requirements.append(f"See {keyword} in description")
                        break
                        
            return {
                "description": description or "Description not available",
                "full_description": description or "Description not available",
                "requirements": requirements,
                "salary": "",  # Already extracted from card
                "job_type": "Contract",
                "experience_level": ""
            }
            
        except Exception as e:
            logger.error(f"Error parsing Upwork job details: {e}")
            return {}
            
    async def cleanup(self):
        """Cleanup Upwork scraper resources"""
        if self.session:
            await self.session.close()
        self.is_initialized = False
        logger.info("Upwork scraper cleaned up")
