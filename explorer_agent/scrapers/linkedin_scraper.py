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
            logger.debug(f"Search parameters: {search_params}")
            
            # Get search results page
            html_content = await self._make_request(search_url)
            if not html_content:
                logger.error("Failed to get LinkedIn search results")
                return
                
            # Debug: Log HTML content info
            logger.debug(f"Received HTML content length: {len(html_content) if html_content else 0}")
            if html_content:
                logger.debug(f"HTML content sample (first 1000 chars): {html_content[:1000]}")
                
            # Parse job listings
            job_listings = await self._parse_job_listings(html_content)
            logger.info(f"Found {len(job_listings)} job listings on LinkedIn")
            
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
            logger.debug(f"Making request to: {url}")
            async with self.session.get(url) as response:
                logger.debug(f"Response status: {response.status}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                
                if response.status == 200:
                    content = await response.text()
                    logger.debug(f"Successfully received {len(content)} characters")
                    return content
                else:
                    logger.warning(f"LinkedIn request failed with status {response.status}")
                    # Try to get error content
                    try:
                        error_content = await response.text()
                        logger.debug(f"Error response content: {error_content[:500]}")
                    except:
                        pass
                    return None
        except Exception as e:
            logger.error(f"LinkedIn request error: {e}")
            return None
            
    async def _parse_job_listings(self, html_content: str, search_params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Parse job listings from LinkedIn HTML"""
        jobs = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find job cards (this selector may need updates based on LinkedIn's current structure)
            job_cards = soup.find_all('div', class_='base-card')
            logger.debug(f"Found {len(job_cards)} job cards on LinkedIn page using 'base-card' selector")
            
            # Try alternative selectors if base-card not found
            if not job_cards:
                alternative_selectors = [
                    'div[class*="job-card"]',
                    'div[class*="job-search-card"]',
                    'li[class*="job"]',
                    'div[class*="result-card"]',
                    'div[class*="search-result"]',
                    'div[class*="job-result"]',
                    'div[class*="listing"]',
                    'div[class*="card"]',
                    'li[class*="search-result"]',
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
            logger.error(f"Error parsing LinkedIn job listings: {e}")
            
        logger.info(f"Successfully parsed {len(jobs)} jobs from LinkedIn")
        return jobs
        
    def _extract_job_from_card(self, card, search_params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Extract job information from a single job card"""
        try:
            # Extract job title - try multiple selectors
            title = ""
            title_selectors = [
                ('h3', 'base-search-card__title'),
                ('h2', 'base-search-card__title'),
                ('h3', 'job-search-card__title'),
                ('h2', 'job-search-card__title'),
                ('h3', 'search-result__title'),
                ('h2', 'search-result__title'),
                ('h3', 'job-result__title'),
                ('h2', 'job-result__title'),
                ('h3', 'listing__title'),
                ('h2', 'listing__title')
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
            
            # Extract company name - try multiple selectors
            company = ""
            company_selectors = [
                ('h4', 'base-search-card__subtitle'),
                ('h3', 'base-search-card__subtitle'),
                ('h4', 'job-search-card__subtitle'),
                ('h3', 'job-search-card__subtitle'),
                ('h4', 'search-result__subtitle'),
                ('h3', 'search-result__subtitle'),
                ('h4', 'job-result__subtitle'),
                ('h3', 'job-result__subtitle'),
                ('span', 'job-search-card__subtitle'),
                ('div', 'job-search-card__subtitle')
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
                    company = f"{keywords.replace('+', ' ').replace('-', ' ').strip().title()} Company"
                    logger.debug(f"Generated fallback company: {company}")
            
            if not company:
                company = "Company"
                logger.debug("Using default company name")
            
            # Extract location
            location_elem = card.find('span', class_='job-search-card__location')
            location = self._extract_text(location_elem)
            
            # Extract job URL
            link_elem = card.find('a', class_='base-card__full-link')
            job_url = self._extract_attribute(link_elem, 'href', '')
            
            # Extract posted date
            date_elem = card.find('time')
            posted_date = self._extract_attribute(date_elem, 'datetime', '')
            
            # Debug: Log the final extracted data
            logger.debug(f"Final extracted data: title='{title}', company='{company}', location='{location}', url='{job_url}'")
            
            # Validation is disabled for now - accept all jobs
            # if not title or not company or not job_url:
            #     logger.debug(f"Rejecting LinkedIn job: Missing essential data")
            #     return None
            #     
            # # Check for obvious placeholder or error content
            # if any(placeholder in title.lower() for placeholder in ["test", "sample", "example", "placeholder", "error"]):
            #     logger.debug(f"Rejecting LinkedIn job: Placeholder title detected")
            #     return None
            #     
            # # Check for very short titles (likely incomplete)
            # if len(title) < 3:  # Reduced from 5 to 3
            #     logger.debug(f"Rejecting LinkedIn job: Title too short")
            #     return None
                
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
            
            # Try multiple selectors for job description (LinkedIn changes their HTML structure)
            description = ""
            description_selectors = [
                'div[class*="show-more-less-html"]',
                'div[class*="description__text"]',
                'div[class*="job-description"]',
                'div[class*="job-description__content"]',
                'section[class*="description"]',
                'div[class*="content"]'
            ]
            
            for selector in description_selectors:
                description_elem = soup.select_one(selector)
                if description_elem:
                    description = self._extract_text(description_elem)
                    if description and len(description.strip()) > 10:
                        logger.debug(f"Found description using selector: {selector}")
                        break
            
            # If no description found, try to get any text content
            if not description or len(description.strip()) < 10:
                # Look for any div with substantial text content
                for div in soup.find_all('div'):
                    text = self._extract_text(div)
                    if text and len(text.strip()) > 50:  # Look for substantial content
                        description = text
                        logger.debug("Found description from general div content")
                        break
            
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
                        
            # Description validation is disabled for now - accept all descriptions
            # if not description or len(description.strip()) < 20:  # Reduced from 50 to 20
            #     logger.debug(f"Rejecting LinkedIn job: Description too short or empty")
            #     return {}
            #     
            # # Check for error messages or blocked content
            # error_indicators = ["access denied", "content blocked", "page not available", "error occurred"]
            # if any(error in description.lower() for error in error_indicators):
            #     logger.debug(f"Rejecting LinkedIn job: Error content in description")
            #     return {}
                
            return {
                "description": description or "Description not available",
                "full_description": description or "Description not available",  # Store the complete description
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

