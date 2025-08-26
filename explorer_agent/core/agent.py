"""
Main Explorer Agent class

Orchestrates job exploration across multiple sources and streams results
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from core.config import get_settings
from scrapers.base_scraper import BaseScraper
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.indeed_scraper import IndeedScraper
from scrapers.glassdoor_scraper import GlassdoorScraper
from processors.job_processor import JobProcessor
from streamers.websocket_manager import WebSocketManager

logger = logging.getLogger(__name__)

class ExplorerAgent:
    """Main agent that explores the internet for job listings"""
    
    def __init__(self):
        self.settings = get_settings()
        self.scrapers: List[BaseScraper] = []
        self.processor: Optional[JobProcessor] = None
        self.websocket_manager: Optional[WebSocketManager] = None
        self.is_running = False
        self.active_searches: Dict[str, asyncio.Task] = {}
        
    async def initialize(self):
        """Initialize the agent and all components"""
        logger.info("Initializing Explorer Agent...")
        
        # Initialize job processor
        self.processor = JobProcessor()
        await self.processor.initialize()
        
        # Initialize scrapers based on configuration
        await self._initialize_scrapers()
        
        # Initialize WebSocket manager
        self.websocket_manager = WebSocketManager()
        
        logger.info("Explorer Agent initialized successfully")
        
    async def _initialize_scrapers(self):
        """Initialize enabled scrapers"""
        if self.settings.enable_linkedin:
            self.scrapers.append(LinkedInScraper())
            
        if self.settings.enable_indeed:
            self.scrapers.append(IndeedScraper())
            
        if self.settings.enable_glassdoor:
            self.scrapers.append(GlassdoorScraper())
            
        if self.settings.enable_stackoverflow:
            # Add StackOverflow scraper when implemented
            pass
            
        logger.info(f"Initialized {len(self.scrapers)} scrapers")
        
    async def explore_jobs(self, websocket, search_params: Optional[Dict] = None):
        """Start exploring jobs and streaming results"""
        if self.is_running:
            logger.warning("Job exploration already running")
            return
            
        self.is_running = True
        search_id = f"search_{datetime.now().isoformat()}"
        
        try:
            # Send initial status
            await websocket.send_json({
                "type": "status",
                "message": "Starting job exploration...",
                "search_id": search_id
            })
            
            # Start exploration tasks for each scraper
            tasks = []
            for scraper in self.scrapers:
                task = asyncio.create_task(
                    self._explore_with_scraper(scraper, websocket, search_params)
                )
                tasks.append(task)
                
            # Wait for all scrapers to complete
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Send completion status
            await websocket.send_json({
                "type": "status",
                "message": "Job exploration completed",
                "search_id": search_id
            })
            
        except Exception as e:
            logger.error(f"Error during job exploration: {e}")
            await websocket.send_json({
                "type": "error",
                "message": f"Error during exploration: {str(e)}",
                "search_id": search_id
            })
        finally:
            self.is_running = False
            
    async def _explore_with_scraper(self, scraper: BaseScraper, websocket, search_params: Optional[Dict] = None):
        """Explore jobs using a specific scraper"""
        try:
            # Send scraper start status
            await websocket.send_json({
                "type": "scraper_status",
                "scraper": scraper.name,
                "status": "starting"
            })
            
            # Track filtering statistics
            total_jobs = 0
            filtered_jobs = 0
            valid_jobs = 0
            
            # Start scraping with streaming
            async for job_data in scraper.scrape_jobs(search_params):
                total_jobs += 1
                
                # Process the job data
                processed_job = await self.processor.process_job(job_data)
                
                # Only stream jobs that passed quality validation
                if processed_job is not None:
                    valid_jobs += 1
                    # Stream the processed job
                    await websocket.send_json({
                        "type": "job_data",
                        "scraper": scraper.name,
                        "data": processed_job
                    })
                    
                    # Rate limiting
                    await asyncio.sleep(self.settings.rate_limit)
                else:
                    filtered_jobs += 1
                    # Log that a job was filtered out
                    logger.debug(f"Job filtered out by quality standards from {scraper.name}")
            
            # Send scraper completion status with filtering statistics
            await websocket.send_json({
                "type": "scraper_status",
                "scraper": scraper.name,
                "status": "completed",
                "stats": {
                    "total_jobs": total_jobs,
                    "valid_jobs": valid_jobs,
                    "filtered_jobs": filtered_jobs,
                    "quality_rate": f"{(valid_jobs/total_jobs*100):.1f}%" if total_jobs > 0 else "0%"
                }
            })
            
            logger.info(f"{scraper.name}: {valid_jobs}/{total_jobs} jobs passed quality filter ({filtered_jobs} filtered out)")
            
        except Exception as e:
            logger.error(f"Error with scraper {scraper.name}: {e}")
            await websocket.send_json({
                "type": "scraper_error",
                "scraper": scraper.name,
                "error": str(e)
            })
            
    async def stop_exploration(self, search_id: str):
        """Stop a specific job exploration"""
        if search_id in self.active_searches:
            task = self.active_searches[search_id]
            task.cancel()
            del self.active_searches[search_id]
            logger.info(f"Stopped exploration {search_id}")
            
    async def get_exploration_status(self) -> Dict[str, Any]:
        """Get current exploration status"""
        return {
            "is_running": self.is_running,
            "active_searches": list(self.active_searches.keys()),
            "enabled_scrapers": [s.name for s in self.scrapers],
            "total_scrapers": len(self.scrapers)
        }
        
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up Explorer Agent...")
        
        # Cancel all active searches
        for search_id, task in self.active_searches.items():
            task.cancel()
            
        # Cleanup processor
        if self.processor:
            await self.processor.cleanup()
            
        logger.info("Explorer Agent cleanup completed")

