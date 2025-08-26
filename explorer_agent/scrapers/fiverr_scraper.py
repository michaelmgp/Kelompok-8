"""
Fiverr gig scraper

Scrapes gig listings from Fiverr's search results
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

class FiverrScraper(BaseScraper):
    """Fiverr Gigs scraper"""
    
    def __init__(self):
        super().__init__()
        self.name = "Fiverr"
        self.base_url = "https://www.fiverr.com"
        self.session = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the Fiverr scraper"""
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
        logger.info("Fiverr scraper initialized")
        
    async def scrape_jobs(self, search_params: Optional[Dict] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Scrape gigs from Fiverr based on search parameters"""
        if not self.is_initialized:
            await self.initialize()
            
        search_params = self._validate_search_params(search_params)
        
        try:
            # Build search URL
            search_url = self._build_search_url(search_params)
            logger.info(f"Searching Fiverr gigs: {search_url}")
            logger.debug(f"Search parameters: {search_params}")
            
            # Get search results page
            html_content = await self._make_request(search_url)
            if not html_content:
                logger.error("Failed to get Fiverr search results")
                return
                
            # Debug: Log HTML content info
            logger.debug(f"Received HTML content length: {len(html_content) if html_content else 0}")
            if html_content:
                logger.debug(f"HTML content sample (first 1000 chars): {html_content[:1000]}")
                
            # Parse gig listings
            gig_listings = await self._parse_gig_listings(html_content)
            logger.info(f"Found {len(gig_listings)} gig listings on Fiverr")
            
            # Yield each gig
            for gig_data in gig_listings:
                # Create job object and yield all gigs (no filtering)
                job_object = self._create_job_object(gig_data)
                if job_object is not None:
                    # Try to get additional gig details if we have a URL
                    if gig_data.get('application_url'):
                        try:
                            logger.debug(f"Getting details for gig: {gig_data.get('title', 'Unknown')}")
                            gig_details = await self.get_job_details(gig_data['application_url'])
                            if gig_details and isinstance(gig_details, dict):
                                # Merge the details with the gig object
                                job_object.update(gig_details)
                                logger.debug(f"Enhanced gig with details: {job_object.get('title', 'Unknown')}")
                        except Exception as e:
                            logger.debug(f"Failed to get gig details: {e}")
                            # Continue with basic gig data
                    
                    yield job_object
                else:
                    logger.debug(f"Job object creation failed for gig data: {gig_data.get('title', 'Unknown')}")
                
                # Rate limiting - be gentle with Fiverr
                await asyncio.sleep(2)
                
        except Exception as e:
            logger.error(f"Error scraping Fiverr gigs: {e}")
            
    async def get_job_details(self, gig_url: str) -> Dict[str, Any]:
        """Get detailed information for a specific Fiverr gig"""
        if not self.is_initialized:
            await self.initialize()
            
        try:
            html_content = await self._make_request(gig_url)
            if not html_content:
                logger.debug(f"No HTML content received for gig URL: {gig_url}")
                return {}
                
            # Parse detailed gig information
            gig_details = await self._parse_gig_details(html_content)
            
            # Accept all gig details (no filtering)
            if not gig_details:
                logger.debug(f"Empty gig details for URL: {gig_url}, but continuing anyway")
                # Return minimal details instead of empty dict
                return {
                    "description": "Description not available",
                    "full_description": "Description not available",
                    "requirements": [],
                    "salary": "",
                    "job_type": "",
                    "experience_level": ""
                }
                
            return self._create_job_object(gig_details)
            
        except Exception as e:
            logger.error(f"Error getting Fiverr gig details: {e}")
            return {}
            
    def _build_search_url(self, search_params: Dict[str, Any]) -> str:
        """Build Fiverr search URL from parameters"""
        base = f"{self.base_url}/search"
        params = []
        
        if search_params.get("keywords"):
            # Fiverr uses query parameter for search
            params.append(f"query={search_params['keywords']}")
            
        if search_params.get("location"):
            # Fiverr might not support location filtering in URL
            logger.debug(f"Location filtering not supported by Fiverr URL: {search_params['location']}")
            
        if search_params.get("experience_level"):
            # Map experience levels to Fiverr's format
            exp_mapping = {
                "entry": "new_seller",
                "junior": "new_seller", 
                "mid-level": "level_one",
                "senior": "level_two",
                "lead": "top_rated"
            }
            exp = exp_mapping.get(search_params['experience_level'].lower(), "new_seller")
            params.append(f"seller_level={exp}")
            
        if search_params.get("job_type"):
            # Fiverr is primarily gig-based
            logger.debug(f"Job type filtering not supported by Fiverr URL: {search_params['job_type']}")
            
        if params:
            return f"{base}?{'&'.join(params)}"
        return base
        
    async def _make_request(self, url: str) -> Optional[str]:
        """Make HTTP request to Fiverr"""
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
                    logger.warning(f"Fiverr request failed with status {response.status}")
                    # Try to get error content
                    try:
                        error_content = await response.text()
                        logger.debug(f"Error response content: {error_content[:500]}")
                    except:
                        pass
                    return None
        except Exception as e:
            logger.error(f"Fiverr request error: {e}")
            return None
            
    async def _parse_gig_listings(self, html_content: str) -> List[Dict[str, Any]]:
        """Parse gig listings from Fiverr HTML"""
        gigs = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find gig cards - Fiverr uses different selectors
            gig_cards = soup.find_all('div', class_='gig-card')
            logger.debug(f"Found {len(gig_cards)} gig cards on Fiverr page using 'gig-card' selector")
            
            # Try alternative selectors if gig-card not found
            if not gig_cards:
                alternative_selectors = [
                    'div[class*="gig"]',
                    'div[class*="search-result"]',
                    'div[class*="card"]',
                    'div[class*="listing"]',
                    'div[class*="result"]',
                    'li[class*="gig"]',
                    'article[class*="gig"]',
                    'div[class*="item"]'
                ]
                for selector in alternative_selectors:
                    gig_cards = soup.select(selector)
                    if gig_cards:
                        logger.debug(f"Found {len(gig_cards)} gigs using alternative selector: {selector}")
                        break
                        
            # If still no gig cards found, log the HTML structure for debugging
            if not gig_cards:
                logger.warning("No gig cards found with any selector. HTML structure might have changed.")
                logger.debug("Available div classes: " + ", ".join([div.get('class', ['no-class'])[0] for div in soup.find_all('div', class_=True)][:20]))
                logger.debug("Available li classes: " + ", ".join([li.get('class', ['no-class'])[0] for li in soup.find_all('li', class_=True)][:20]))
            
            for i, card in enumerate(gig_cards):
                try:
                    gig_data = self._extract_gig_from_card(card, search_params)
                    if gig_data:
                        gigs.append(gig_data)
                        logger.debug(f"Successfully parsed gig {i+1}: {gig_data.get('title', 'Unknown')}")
                    else:
                        logger.debug(f"Failed to parse gig card {i+1}")
                except Exception as e:
                    logger.debug(f"Error parsing gig card {i+1}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Fiverr gig listings: {e}")
            
        logger.info(f"Successfully parsed {len(gigs)} gigs from Fiverr")
        return gigs
        
    def _extract_gig_from_card(self, card, search_params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Extract gig information from a single Fiverr gig card"""
        try:
            # Extract gig title - try multiple selectors
            title = ""
            title_selectors = [
                ('h3', 'gig-title'),
                ('h2', 'gig-title'),
                ('h4', 'gig-title'),
                ('h3', 'title'),
                ('h2', 'title'),
                ('h4', 'title'),
                ('a', 'gig-title'),
                ('span', 'gig-title')
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
                logger.warning(f"No title found for gig card. Available elements: {[elem.name for elem in card.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]}")
                return None
            
            # Extract seller name (equivalent to company)
            company = ""
            company_selectors = [
                ('span', 'seller-name'),
                ('div', 'seller-name'),
                ('a', 'seller-name'),
                ('span', 'username'),
                ('div', 'username'),
                ('a', 'username'),
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
                    company = f"{keywords.replace('+', ' ').replace('-', ' ').strip().title()} Seller"
                    logger.debug(f"Generated fallback company: {company}")
            
            if not company:
                company = "Seller"
                logger.debug("Using default company name")
            
            # Extract location (might not be available on Fiverr)
            location = ""
            location_elem = card.find('span', class_='location')
            if location_elem:
                location = self._extract_text(location_elem)
            
            # Extract gig URL
            gig_url = ""
            link_elem = card.find('a', href=True)
            if link_elem:
                gig_url = link_elem.get('href')
                if not gig_url.startswith('http'):
                    gig_url = self.base_url + gig_url
            
            # Extract price/budget
            salary = ""
            price_elem = card.find('span', class_='price')
            if price_elem:
                salary = self._extract_text(price_elem)
            
            # Extract posted date (might not be available on Fiverr)
            posted_date = ""
            date_elem = card.find('time')
            if date_elem:
                posted_date = self._extract_attribute(date_elem, 'datetime', '')
            
            # Debug: Log the final extracted data
            logger.debug(f"Final extracted data: title='{title}', company='{company}', location='{location}', url='{gig_url}'")
            
            return {
                "id": gig_url.split('/')[-1] if gig_url else "",
                "title": title,
                "company": company,
                "location": location or "Remote",  # Fiverr is mostly remote
                "description": "",  # Will be filled in get_job_details
                "requirements": [],
                "salary": salary,
                "job_type": "Gig",  # Fiverr is gig-based
                "experience_level": "Mid-level",
                "posted_date": posted_date,
                "application_url": gig_url,
                "original_url": gig_url,
                "full_description": "",  # Will be filled in get_job_details
                "extracted_skills": [],  # Will be populated by processor
                "raw_data": {
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": gig_url,
                    "salary": salary
                }
            }
            
        except Exception as e:
            logger.debug(f"Error extracting gig from card: {e}")
            return None
            
    async def _parse_gig_details(self, html_content: str) -> Dict[str, Any]:
        """Parse detailed gig information from Fiverr gig page"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try multiple selectors for gig description
            description = ""
            description_selectors = [
                'div[class*="gig-description"]',
                'div[class*="description"]',
                'div[class*="content"]',
                'section[class*="description"]',
                'div[class*="gig-details"]'
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
            requirements_elem = soup.find('div', class_='gig-requirements')
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
                "job_type": "Gig",
                "experience_level": ""
            }
            
        except Exception as e:
            logger.error(f"Error parsing Fiverr gig details: {e}")
            return {}
            
    async def cleanup(self):
        """Cleanup Fiverr scraper resources"""
        if self.session:
            await self.session.close()
        self.is_initialized = False
        logger.info("Fiverr scraper cleaned up")
