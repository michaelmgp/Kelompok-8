import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiohttp
import time
from collections import defaultdict

from agents.coordinator import Coordinator, UnifiedJob

logger = logging.getLogger(__name__)

@dataclass
class ScrapingTask:
    """Represents a scraping task"""
    id: str
    query: str
    category: Optional[str]
    skills: Optional[List[str]]
    platforms: List[str]
    priority: int  # Higher number = higher priority
    created_at: datetime
    scheduled_for: datetime
    max_results: int
    callback: Optional[Callable] = None

@dataclass
class ScrapingResult:
    """Result of a scraping task"""
    task_id: str
    jobs_found: List[UnifiedJob]
    platforms_searched: List[str]
    start_time: datetime
    end_time: datetime
    success: bool
    error_message: Optional[str] = None

class JobScraper:
    """
    Orchestrates job scraping across multiple platforms
    """
    
    def __init__(self, coordinator: Coordinator, config: Dict[str, Any]):
        self.coordinator = coordinator
        self.config = config
        self.tasks: List[ScrapingTask] = []
        self.results: Dict[str, ScrapingResult] = {}
        self.is_running = False
        self.rate_limits = self._setup_rate_limits()
        self.task_queue = asyncio.Queue()
        self.worker_tasks = []
        
    def _setup_rate_limits(self) -> Dict[str, Dict[str, Any]]:
        """Setup rate limiting configuration for each platform"""
        return {
            "upwork": {
                "requests_per_minute": 60,
                "requests_per_hour": 1000,
                "last_request": None,
                "request_count": 0,
                "hour_count": 0,
                "hour_reset": datetime.utcnow()
            },
            "fiverr": {
                "requests_per_minute": 120,
                "requests_per_hour": 2000,
                "last_request": None,
                "request_count": 0,
                "hour_count": 0,
                "hour_reset": datetime.utcnow()
            }
        }
    
    async def start(self, worker_count: int = 3):
        """Start the scraper with specified number of workers"""
        if self.is_running:
            logger.warning("Scraper is already running")
            return
        
        self.is_running = True
        logger.info(f"Starting job scraper with {worker_count} workers")
        
        # Start worker tasks
        for i in range(worker_count):
            worker_task = asyncio.create_task(self._worker(f"worker-{i}"))
            self.worker_tasks.append(worker_task)
        
        # Start task processor
        processor_task = asyncio.create_task(self._task_processor())
        self.worker_tasks.append(processor_task)
        
        logger.info("Job scraper started successfully")
    
    async def stop(self):
        """Stop the scraper"""
        if not self.is_running:
            return
        
        self.is_running = False
        logger.info("Stopping job scraper...")
        
        # Cancel all worker tasks
        for task in self.worker_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
        
        logger.info("Job scraper stopped")
    
    async def add_task(
        self,
        query: str,
        category: Optional[str] = None,
        skills: Optional[List[str]] = None,
        platforms: List[str] = None,
        priority: int = 1,
        scheduled_for: Optional[datetime] = None,
        max_results: int = 50,
        callback: Optional[Callable] = None
    ) -> str:
        """Add a new scraping task"""
        if platforms is None:
            platforms = ["upwork", "fiverr"]
        
        if scheduled_for is None:
            scheduled_for = datetime.utcnow()
        
        task_id = f"task_{int(time.time())}_{hash(query)}"
        
        task = ScrapingTask(
            id=task_id,
            query=query,
            category=category,
            skills=skills,
            platforms=platforms,
            priority=priority,
            created_at=datetime.utcnow(),
            scheduled_for=scheduled_for,
            max_results=max_results,
            callback=callback
        )
        
        self.tasks.append(task)
        await self.task_queue.put(task)
        
        logger.info(f"Added scraping task: {task_id} for query: {query}")
        return task_id
    
    async def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        # Check if task exists
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            return None
        
        # Check if result exists
        result = self.results.get(task_id)
        
        return {
            "task_id": task_id,
            "query": task.query,
            "status": "completed" if result else "pending",
            "created_at": task.created_at.isoformat(),
            "scheduled_for": task.scheduled_for.isoformat(),
            "priority": task.priority,
            "result": result.to_dict() if result else None
        }
    
    async def _task_processor(self):
        """Process tasks from the queue"""
        while self.is_running:
            try:
                # Get task from queue
                task = await asyncio.wait_for(
                    self.task_queue.get(), timeout=1.0
                )
                
                # Check if task is ready to execute
                if datetime.utcnow() >= task.scheduled_for:
                    # Execute task
                    await self._execute_task(task)
                else:
                    # Re-queue for later execution
                    await asyncio.sleep(1)
                    await self.task_queue.put(task)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in task processor: {e}")
    
    async def _worker(self, worker_name: str):
        """Worker task that processes scraping jobs"""
        logger.info(f"Worker {worker_name} started")
        
        while self.is_running:
            try:
                # Process tasks
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in worker {worker_name}: {e}")
        
        logger.info(f"Worker {worker_name} stopped")
    
    async def _execute_task(self, task: ScrapingTask):
        """Execute a scraping task"""
        logger.info(f"Executing task {task.id}: {task.query}")
        
        start_time = datetime.utcnow()
        jobs_found = []
        platforms_searched = []
        success = True
        error_message = None
        
        try:
            # Check rate limits before proceeding
            await self._check_rate_limits(task.platforms)
            
            # Execute search across platforms
            for platform in task.platforms:
                try:
                    if platform == "upwork":
                        platform_jobs = await self._scrape_upwork(
                            task.query, task.category, task.skills, task.max_results
                        )
                    elif platform == "fiverr":
                        platform_jobs = await self._scrape_fiverr(
                            task.query, task.category, task.skills, task.max_results
                        )
                    else:
                        logger.warning(f"Unknown platform: {platform}")
                        continue
                    
                    jobs_found.extend(platform_jobs)
                    platforms_searched.append(platform)
                    
                    # Update rate limits
                    self._update_rate_limits(platform)
                    
                except Exception as e:
                    logger.error(f"Error scraping {platform}: {e}")
                    error_message = f"Failed to scrape {platform}: {str(e)}"
                    success = False
            
            # Sort jobs by AI score
            jobs_found.sort(key=lambda x: x.ai_score, reverse=True)
            
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {e}")
            success = False
            error_message = str(e)
        
        end_time = datetime.utcnow()
        
        # Create result
        result = ScrapingResult(
            task_id=task.id,
            jobs_found=jobs_found,
            platforms_searched=platforms_searched,
            start_time=start_time,
            end_time=end_time,
            success=success,
            error_message=error_message
        )
        
        # Store result
        self.results[task.id] = result
        
        # Execute callback if provided
        if task.callback and callable(task.callback):
            try:
                await task.callback(result)
            except Exception as e:
                logger.error(f"Error executing callback for task {task.id}: {e}")
        
        logger.info(f"Task {task.id} completed: {len(jobs_found)} jobs found")
    
    async def _scrape_upwork(
        self, 
        query: str, 
        category: Optional[str], 
        skills: Optional[List[str]], 
        max_results: int
    ) -> List[UnifiedJob]:
        """Scrape jobs from Upwork"""
        if not self.coordinator.upwork_agent:
            return []
        
        return await self.coordinator.upwork_agent.search_jobs(
            query, category, skills, max_results
        )
    
    async def _scrape_fiverr(
        self, 
        query: str, 
        category: Optional[str], 
        skills: Optional[List[str]], 
        max_results: int
    ) -> List[UnifiedJob]:
        """Scrape gigs from Fiverr"""
        if not self.coordinator.fiverr_agent:
            return []
        
        return await self.coordinator.fiverr_agent.search_gigs(
            query, category, None, max_results
        )
    
    async def _check_rate_limits(self, platforms: List[str]):
        """Check rate limits for platforms"""
        for platform in platforms:
            if platform not in self.rate_limits:
                continue
            
            limits = self.rate_limits[platform]
            now = datetime.utcnow()
            
            # Reset hourly counter if needed
            if now - limits["hour_reset"] > timedelta(hours=1):
                limits["hour_count"] = 0
                limits["hour_reset"] = now
            
            # Check minute limit
            if limits["last_request"]:
                time_since_last = (now - limits["last_request"]).total_seconds()
                if time_since_last < 60 and limits["request_count"] >= limits["requests_per_minute"]:
                    wait_time = 60 - time_since_last
                    logger.info(f"Rate limit hit for {platform}, waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                    limits["request_count"] = 0
            
            # Check hour limit
            if limits["hour_count"] >= limits["requests_per_hour"]:
                wait_time = 3600  # 1 hour
                logger.info(f"Hourly rate limit hit for {platform}, waiting {wait_time}s")
                await asyncio.sleep(wait_time)
                limits["hour_count"] = 0
    
    def _update_rate_limits(self, platform: str):
        """Update rate limit counters"""
        if platform not in self.rate_limits:
            return
        
        limits = self.rate_limits[platform]
        now = datetime.utcnow()
        
        limits["last_request"] = now
        limits["request_count"] += 1
        limits["hour_count"] += 1
    
    async def get_scraping_stats(self) -> Dict[str, Any]:
        """Get scraping statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len(self.results)
        pending_tasks = total_tasks - completed_tasks
        
        total_jobs = sum(len(r.jobs_found) for r in self.results.values())
        
        platform_stats = defaultdict(lambda: {"jobs_found": 0, "tasks_executed": 0})
        
        for result in self.results.values():
            for platform in result.platforms_searched:
                platform_stats[platform]["jobs_found"] += len(
                    [j for j in result.jobs_found if j.platform == platform]
                )
                platform_stats[platform]["tasks_executed"] += 1
        
        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "total_jobs_found": total_jobs,
            "platform_stats": dict(platform_stats),
            "rate_limits": self.rate_limits
        }
    
    async def cleanup(self):
        """Cleanup scraper resources"""
        await self.stop()
        
        # Clear data
        self.tasks.clear()
        self.results.clear()
        
        logger.info("Job scraper cleanup completed") 