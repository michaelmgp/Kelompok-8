#!/usr/bin/env python3
"""
Remote.co Scraper

Scrapes job listings from Remote.co with fallback title logic.
If no title is found, generates a title based on search keywords.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, AsyncGenerator
from urllib.parse import urlencode, quote
import aiohttp
from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class RemoteCoScraper(BaseScraper):
    """Scraper for Remote.co"""
    
    name = "RemoteCoScraper"
    base_url = "https://remote.co"
    
    def __init__(self):
        self.session = None
        
    async def initialize(self):
        """Initialize the scraper session"""
        self.session = aiohttp.ClientSession(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        
    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            
    async def scrape_jobs(self, search_params: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Scrape jobs from Remote.co"""
        try:
            search_url = self._build_search_url(search_params)
            logger.info(f"Scraping Remote.co: {search_url}")
            
            # Get search results
            html_content = await self._make_request(search_url)
            if not html_content:
                return
                
            # Parse job listings
            async for job_data in self._parse_job_listings(html_content, search_params):
                if job_data:
                    yield job_data
                    
        except Exception as e:
            logger.error(f"Error scraping Remote.co: {e}")
            
    async def get_job_details(self, job_url: str) -> Optional[Dict[str, Any]]:
        """Get detailed job information"""
        try:
            html_content = await self._make_request(job_url)
            if not html_content:
                return None
                
            return await self._parse_job_details(html_content)
            
        except Exception as e:
            logger.error(f"Error getting job details from {job_url}: {e}")
            return None
            
    def _build_search_url(self, search_params: Dict[str, Any]) -> str:
        """Build Remote.co search URL"""
        params = {}
        
        # Map search parameters to Remote.co format
        if search_params.get('keywords'):
            params['search'] = search_params['keywords']
            
        if search_params.get('location'):
            # Remote.co is primarily remote, but can filter by location
            if 'remote' not in search_params['location'].lower():
                params['location'] = search_params['location']
                
        if search_params.get('job_type'):
            job_type = search_params['job_type'].lower()
            if 'full-time' in job_type:
                params['type'] = 'full-time'
            elif 'part-time' in job_type:
                params['type'] = 'part-time'
            elif 'contract' in job_type:
                params['type'] = 'contract'
                
        if search_params.get('experience_level'):
            exp = search_params['experience_level'].lower()
            if 'entry' in exp or 'junior' in exp:
                params['level'] = 'entry'
            elif 'senior' in exp:
                params['level'] = 'senior'
                
        # Build URL
        query_string = urlencode(params) if params else ''
        return f"{self.base_url}/remote-jobs/search?{query_string}"
        
    async def _make_request(self, url: str) -> Optional[str]:
        """Make HTTP request to Remote.co"""
        try:
            async with self.session.get(url) as response:
                logger.debug(f"Remote.co request: {response.status} - {url}")
                
                if response.status == 200:
                    content = await response.text()
                    logger.debug(f"Remote.co response length: {len(content)}")
                    return content
                else:
                    logger.warning(f"Remote.co request failed: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error making request to {url}: {e}")
            return None
            
    async def _parse_job_listings(self, html_content: str, search_params: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Parse job listings from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find job cards - Remote.co uses various selectors
            job_cards = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['job', 'listing', 'card', 'item', 'post']
            ))
            
            logger.debug(f"Found {len(job_cards)} job cards on Remote.co")
            
            for card in job_cards:
                try:
                    job_data = await self._extract_job_from_card(card, search_params)
                    if job_data:
                        yield job_data
                        
                except Exception as e:
                    logger.debug(f"Error extracting job from card: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Remote.co job listings: {e}")
            
    async def _extract_job_from_card(self, card, search_params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract job data from a job card"""
        try:
            # Try multiple selectors for title
            title = None
            title_selectors = [
                'h2 a', 'h3 a', 'h4 a', '.job-title', '.title', 
                'a[href*="/remote-jobs/"]', '[class*="title"]', '.job-link'
            ]
            
            for selector in title_selectors:
                title_elem = card.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title:
                        break
                        
            # Fallback: generate title from keywords if none found
            if not title:
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
                return None
                
            # Extract company name
            company = None
            company_selectors = [
                '.company', '.employer', '.client', '[class*="company"]', 
                '[class*="employer"]', 'a[href*="/companies/"]', '.author'
            ]
            
            for selector in company_selectors:
                company_elem = card.select_one(selector)
                if company_elem:
                    company = company_elem.get_text(strip=True)
                    if company:
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
                        
            # Extract location (Remote.co is primarily remote)
            location = 'Remote'  # Default to remote
            location_selectors = [
                '.location', '.city', '.country', '[class*="location"]',
                '[class*="city"]', '[class*="country"]'
            ]
            
            for selector in location_selectors:
                location_elem = card.select_one(selector)
                if location_elem:
                    loc_text = location_elem.get_text(strip=True)
                    if loc_text and loc_text.lower() != 'remote':
                        location = loc_text
                        break
                        
            # Extract job URL
            job_url = None
            url_selectors = [
                'h2 a', 'h3 a', 'h4 a', '.job-title a', 'a[href*="/remote-jobs/"]', '.job-link'
            ]
            
            for selector in url_selectors:
                url_elem = card.select_one(selector)
                if url_elem and url_elem.get('href'):
                    href = url_elem.get('href')
                    if href.startswith('/'):
                        job_url = f"{self.base_url}{href}"
                    else:
                        job_url = href
                    break
                    
            # Extract salary (if available)
            salary = None
            salary_selectors = [
                '.salary', '.compensation', '[class*="salary"]', '[class*="comp"]', '.rate'
            ]
            
            for selector in salary_selectors:
                salary_elem = card.select_one(selector)
                if salary_elem:
                    salary = salary_elem.get_text(strip=True)
                    if salary:
                        break
                        
            # Extract posted date
            posted_date = None
            date_selectors = [
                '.date', '.posted', '.time', '[class*="date"]', '[class*="time"]', '.meta'
            ]
            
            for selector in date_selectors:
                date_elem = card.select_one(selector)
                if date_elem:
                    posted_date = date_elem.get_text(strip=True)
                    if posted_date:
                        break
                        
            # Build job data
            job_data = {
                'title': title,
                'company': company or 'Unknown Company',
                'location': location,
                'application_url': job_url or '',
                'salary': salary,
                'posted_date': posted_date,
                'source': 'Remote.co',
                'platform': 'remoteco'
            }
            
            logger.debug(f"Extracted Remote.co job: {title} at {company}")
            return job_data
            
        except Exception as e:
            logger.debug(f"Error extracting Remote.co job data: {e}")
            return None
            
    async def _parse_job_details(self, html_content: str) -> Optional[Dict[str, Any]]:
        """Parse detailed job description"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract job description
            description = None
            desc_selectors = [
                '.job-description', '.description', '.content', 
                '[class*="description"]', '[class*="content"]', '.entry-content'
            ]
            
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                    if description:
                        break
                        
            return {
                'description': description or 'No description available',
                'full_html': html_content
            }
            
        except Exception as e:
            logger.error(f"Error parsing Remote.co job details: {e}")
            return None
