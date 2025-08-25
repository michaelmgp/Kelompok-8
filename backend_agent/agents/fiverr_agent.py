import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import aiohttp
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity

logger = logging.getLogger(__name__)

@dataclass
class FiverrJob:
    id: str
    title: str
    description: str
    price: Optional[str]
    category: str
    seller_info: Dict[str, Any]
    rating: Optional[float]
    review_count: Optional[int]
    delivery_time: Optional[str]
    url: str
    ai_score: Optional[float] = None

class FiverrAgent:
    """
    Fetch.ai agent for Fiverr gig discovery and analysis
    """
    
    def __init__(self, api_key: str, entity: Entity):
        self.api_key = api_key
        self.entity = entity
        self.ledger_api = LedgerApi("https://rest.fetch.ai")
        self.session = None
        self.base_url = "https://api.fiverr.com/v1"
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "JobPlatformBot/1.0"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_gigs(
        self, 
        query: str, 
        category: str = None,
        subcategory: str = None,
        limit: int = 50
    ) -> List[FiverrJob]:
        """
        Search for gigs on Fiverr based on criteria
        """
        try:
            params = {
                "query": query,
                "limit": limit,
                "offset": 0
            }
            
            if category:
                params["category"] = category
            if subcategory:
                params["subcategory"] = subcategory
                
            async with self.session.get(
                f"{self.base_url}/search/gigs",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    gigs = []
                    
                    for gig_data in data.get("gigs", []):
                        gig = self._parse_gig_data(gig_data)
                        if gig:
                            # Apply AI scoring
                            gig.ai_score = await self._calculate_ai_score(gig)
                            gigs.append(gig)
                    
                    logger.info(f"Found {len(gigs)} gigs for query: {query}")
                    return gigs
                else:
                    logger.error(f"Failed to fetch gigs: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching Fiverr gigs: {e}")
            return []
    
    def _parse_gig_data(self, gig_data: Dict[str, Any]) -> Optional[FiverrJob]:
        """
        Parse raw gig data into FiverrJob object
        """
        try:
            return FiverrJob(
                id=gig_data.get("id"),
                title=gig_data.get("title", ""),
                description=gig_data.get("description", ""),
                price=gig_data.get("price", {}).get("amount"),
                category=gig_data.get("category", {}).get("name", ""),
                seller_info={
                    "username": gig_data.get("seller", {}).get("username"),
                    "level": gig_data.get("seller", {}).get("level"),
                    "country": gig_data.get("seller", {}).get("country"),
                    "response_time": gig_data.get("seller", {}).get("response_time")
                },
                rating=gig_data.get("rating"),
                review_count=gig_data.get("review_count"),
                delivery_time=gig_data.get("delivery_time"),
                url=f"https://www.fiverr.com{gig_data.get('url', '')}"
            )
        except Exception as e:
            logger.error(f"Error parsing gig data: {e}")
            return None
    
    async def _calculate_ai_score(self, gig: FiverrJob) -> float:
        """
        Calculate AI-powered relevance score for a gig
        """
        try:
            score = 0.0
            
            # Rating scoring
            if gig.rating:
                score += min(gig.rating * 0.2, 0.4)
            
            # Review count scoring
            if gig.review_count:
                if gig.review_count > 100:
                    score += 0.2
                elif gig.review_count > 50:
                    score += 0.15
                elif gig.review_count > 10:
                    score += 0.1
            
            # Seller level scoring
            if gig.seller_info.get("level"):
                level = gig.seller_info["level"]
                if level == "Top Rated":
                    score += 0.2
                elif level == "Level 2":
                    score += 0.15
                elif level == "Level 1":
                    score += 0.1
            
            # Response time scoring
            if gig.seller_info.get("response_time"):
                response_time = gig.seller_info["response_time"]
                if response_time == "1 hour":
                    score += 0.1
                elif response_time == "2 hours":
                    score += 0.05
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating AI score: {e}")
            return 0.0
    
    async def get_gig_details(self, gig_id: str) -> Optional[FiverrJob]:
        """
        Get detailed information for a specific gig
        """
        try:
            async with self.session.get(
                f"{self.base_url}/gigs/{gig_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_gig_data(data)
                else:
                    logger.error(f"Failed to fetch gig details: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching gig details: {e}")
            return None
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """
        Get available categories and subcategories
        """
        try:
            async with self.session.get(
                f"{self.base_url}/categories"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("categories", [])
                else:
                    logger.error(f"Failed to fetch categories: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return []
    
    async def get_trending_gigs(self, category: str = None) -> List[FiverrJob]:
        """
        Get trending gigs in a category
        """
        try:
            params = {}
            if category:
                params["category"] = category
                
            async with self.session.get(
                f"{self.base_url}/trending/gigs",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    gigs = []
                    
                    for gig_data in data.get("gigs", []):
                        gig = self._parse_gig_data(gig_data)
                        if gig:
                            gig.ai_score = await self._calculate_ai_score(gig)
                            gigs.append(gig)
                    
                    return gigs
                else:
                    logger.error(f"Failed to fetch trending gigs: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching trending gigs: {e}")
            return [] 