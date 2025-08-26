#!/usr/bin/env python3
"""
Stack Overflow Jobs Scraper

Scrapes job listings from Stack Overflow Jobs with fallback title logic.
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

class StackOverflowScraper(BaseScraper):
    """Scraper for Stack Overflow Jobs"""
    
    name = "StackOverflowScraper"
    base_url = "https://stackoverflow.com"
    
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
        """Scrape jobs from Stack Overflow"""
        try:
            search_url = self._build_search_url(search_params)
            logger.info(f"Scraping Stack Overflow Jobs: {search_url}")
            
            # Get search results
            html_content = await self._make_request(search_url)
            if not html_content:
                return
                
            # Parse job listings
            async for job_data in self._parse_job_listings(html_content, search_params):
                if job_data:
                    yield job_data
                    
        except Exception as e:
            logger.error(f"Error scraping Stack Overflow Jobs: {e}")
            
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
        """Build Stack Overflow Jobs search URL"""
        params = {}
        
        # Map search parameters to Stack Overflow format
        if search_params.get('keywords'):
            params['q'] = search_params['keywords']
            
        if search_params.get('location'):
            params['l'] = search_params['location']
            
        if search_params.get('job_type'):
            # Map job types to Stack Overflow categories
            job_type = search_params['job_type'].lower()
            if 'remote' in job_type:
                params['r'] = 'true'
            elif 'full-time' in job_type:
                params['f'] = 'true'
            elif 'part-time' in job_type:
                params['p'] = 'true'
                
        if search_params.get('experience_level'):
            # Map experience levels
            exp = search_params['experience_level'].lower()
            if 'entry' in exp or 'junior' in exp:
                params['e'] = 'entry'
            elif 'senior' in exp:
                params['e'] = 'senior'
                
        # Build URL
        query_string = urlencode(params) if params else ''
        return f"{self.base_url}/jobs?{query_string}"
        
    async def _make_request(self, url: str) -> Optional[str]:
        """Make HTTP request to Stack Overflow"""
        try:
            async with self.session.get(url) as response:
                logger.debug(f"Stack Overflow request: {response.status} - {url}")
                
                if response.status == 200:
                    content = await response.text()
                    logger.debug(f"Stack Overflow response length: {len(content)}")
                    return content
                else:
                    logger.warning(f"Stack Overflow request failed: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error making request to {url}: {e}")
            return None
            
    async def _parse_job_listings(self, html_content: str, search_params: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Parse job listings from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find job cards - Stack Overflow uses various selectors
            job_cards = soup.find_all(['div', 'article'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['job', 'listing', 'card', 'item']
            ))
            
            logger.debug(f"Found {len(job_cards)} job cards on Stack Overflow")
            
            for card in job_cards:
                try:
                    job_data = await self._extract_job_from_card(card, search_params)
                    if job_data:
                        yield job_data
                        
                except Exception as e:
                    logger.debug(f"Error extracting job from card: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Stack Overflow job listings: {e}")
            
    async def _extract_job_from_card(self, card, search_params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract job data from a job card"""
        try:
            # Try multiple selectors for title
            title = None
            title_selectors = [
                'h2 a', 'h3 a', 'h4 a', '.job-title', '.title', 
                'a[href*="/jobs/"]', '[class*="title"]'
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
                '[class*="employer"]', 'a[href*="/companies/"]'
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
                        
            # Extract location
            location = None
            location_selectors = [
                '.location', '.city', '.country', '[class*="location"]',
                '[class*="city"]', '[class*="country"]'
            ]
            
            for selector in location_selectors:
                location_elem = card.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    if location:
                        break
                        
            # Extract job URL
            job_url = None
            url_selectors = [
                'h2 a', 'h3 a', 'h4 a', '.job-title a', 'a[href*="/jobs/"]'
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
                '.salary', '.compensation', '[class*="salary"]', '[class*="comp"]'
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
                '.date', '.posted', '.time', '[class*="date"]', '[class*="time"]'
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
                'location': location or 'Remote',
                'application_url': job_url or '',
                'salary': salary,
                'posted_date': posted_date,
                'source': 'Stack Overflow Jobs',
                'platform': 'stackoverflow'
            }
            
            logger.debug(f"Extracted Stack Overflow job: {title} at {company}")
            return job_data
            
        except Exception as e:
            logger.debug(f"Error extracting Stack Overflow job data: {e}")
            return None
            
    async def _parse_job_details(self, html_content: str) -> Optional[Dict[str, Any]]:
        """Parse detailed job description"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract job description
            description = None
            desc_selectors = [
                '.job-description', '.description', '.content', 
                '[class*="description"]', '[class*="content"]'
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
            logger.error(f"Error parsing Stack Overflow job details: {e}")
            return None
