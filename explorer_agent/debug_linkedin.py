#!/usr/bin/env python3
"""
Debug script for LinkedIn scraper
Run this to see what's happening with job extraction
"""

import asyncio
import logging
from scrapers.linkedin_scraper import LinkedInScraper

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_linkedin_scraper():
    """Test the LinkedIn scraper to see what's happening"""
    scraper = LinkedInScraper()
    await scraper.initialize()
    
    # Test with simple search
    search_params = {
        "keywords": "python developer",
        "location": "remote",
        "limit": 5
    }
    
    logger.info("Testing LinkedIn scraper...")
    
    try:
        job_count = 0
        async for job_data in scraper.scrape_jobs(search_params):
            job_count += 1
            logger.info(f"=== Job {job_count} ===")
            logger.info(f"Title: {job_data.get('title', 'NO TITLE')}")
            logger.info(f"Company: {job_data.get('company', 'NO COMPANY')}")
            logger.info(f"Location: {job_data.get('location', 'NO LOCATION')}")
            logger.info(f"URL: {job_data.get('application_url', 'NO URL')}")
            logger.info(f"Full data: {job_data}")
            logger.info("=" * 30)
            
            if job_count >= 3:  # Just test first 3 jobs
                break
                
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
    
    await scraper.cleanup()

if __name__ == "__main__":
    asyncio.run(test_linkedin_scraper())
