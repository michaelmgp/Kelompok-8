#!/usr/bin/env python3
"""
Test script for all job scrapers

Tests the fallback title logic and verifies all scrapers are working.
"""

import asyncio
import logging
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.upwork_scraper import UpworkScraper
from scrapers.fiverr_scraper import FiverrScraper
from scrapers.stackoverflow_scraper import StackOverflowScraper
from scrapers.remoteco_scraper import RemoteCoScraper
from scrapers.weworkremotely_scraper import WeWorkRemotelyScraper

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_scraper(scraper_class, scraper_name, search_params):
    """Test a single scraper"""
    try:
        logger.info(f"Testing {scraper_name}...")
        scraper = scraper_class()
        await scraper.initialize()
        
        # Test scraping
        job_count = 0
        async for job_data in scraper.scrape_jobs(search_params):
            job_count += 1
            logger.info(f"  {scraper_name}: {job_data.get('title', 'NO TITLE')} at {job_data.get('company', 'NO COMPANY')}")
            
            if job_count >= 2:  # Just test first 2 jobs per scraper
                break
                
        logger.info(f"  {scraper_name}: Found {job_count} jobs")
        await scraper.cleanup()
        
    except Exception as e:
        logger.error(f"  {scraper_name}: Error - {e}")

async def test_fallback_titles():
    """Test fallback title generation"""
    logger.info("Testing fallback title logic...")
    
    # Test with different keywords
    test_cases = [
        {"keywords": "java developer", "expected": "Java Developer"},
        {"keywords": "python", "expected": "Python Developer"},
        {"keywords": "react frontend", "expected": "React Frontend Professional"},
        {"keywords": "data scientist", "expected": "Data Scientist Professional"}
    ]
    
    for test_case in test_cases:
        keywords = test_case["keywords"]
        expected = test_case["expected"]
        
        # Test programming language detection
        programming_languages = ['java', 'python', 'javascript', 'react', 'node', 'php', 'c#', 'c++', 'go', 'rust', 'swift', 'kotlin']
        if any(lang in keywords.lower() for lang in programming_languages):
            generated_title = f"{keywords.title()} Developer"
        else:
            generated_title = f"{keywords.title()} Professional"
            
        logger.info(f"  Keywords: '{keywords}' -> Generated: '{generated_title}' (Expected: '{expected}')")
    
    # Test company fallback logic
    logger.info("Testing company fallback logic...")
    test_keywords = ["java", "python developer", "react"]
    for keywords in test_keywords:
        company = f"{keywords.replace('+', ' ').replace('-', ' ').strip().title()} Company"
        logger.info(f"  Keywords: '{keywords}' -> Company: '{company}'")

async def main():
    """Main test function"""
    logger.info("Starting scraper tests...")
    
    # Test fallback title logic
    await test_fallback_titles()
    
    # Test search parameters
    search_params = {
        "keywords": "python developer",
        "location": "remote",
        "job_type": "full-time",
        "experience_level": "mid-level"
    }
    
    # Test all scrapers
    scrapers = [
        (LinkedInScraper, "LinkedIn"),
        (UpworkScraper, "Upwork"),
        (FiverrScraper, "Fiverr"),
        (StackOverflowScraper, "Stack Overflow"),
        (RemoteCoScraper, "Remote.co"),
        (WeWorkRemotelyScraper, "WeWorkRemotely")
    ]
    
    for scraper_class, scraper_name in scrapers:
        await test_scraper(scraper_class, scraper_name, search_params)
        await asyncio.sleep(1)  # Small delay between scrapers
        
    logger.info("All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
