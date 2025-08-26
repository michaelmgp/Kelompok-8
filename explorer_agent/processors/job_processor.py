"""
Job data processor

Handles data cleaning, validation, and AI-powered analysis of job listings
"""

import logging
from typing import Dict, Any, Optional, List
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class JobProcessor:
    """Processes and analyzes job data"""
    
    def __init__(self):
        self.ai_enabled = False
        self.ai_client = None
        
    async def initialize(self):
        """Initialize the job processor"""
        # TODO: Initialize AI client if configured
        logger.info("Job processor initialized")
        
    async def process_job(self, job_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process and clean job data, return None if job doesn't meet quality standards"""
        try:
            # Clean and validate the job data
            cleaned_job = self._clean_job_data(job_data)
            
            # Apply quality filter - reject low-quality jobs
            if not self._validate_job_quality(cleaned_job):
                logger.info(f"Job rejected due to quality issues: {cleaned_job.get('title', 'Unknown')}")
                return None
            
            # Enrich with additional analysis
            enriched_job = await self._enrich_job_data(cleaned_job)
            
            # Add processing metadata
            enriched_job["processed_at"] = datetime.now().isoformat()
            enriched_job["processing_version"] = "1.0.0"
            
            logger.info(f"Job processed successfully: {enriched_job.get('title', 'Unknown')} at {enriched_job.get('company', 'Unknown')}")
            return enriched_job
            
        except Exception as e:
            logger.error(f"Error processing job data: {e}")
            return None
            
    def _clean_job_data(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate job data"""
        cleaned = job_data.copy()
        
        # Clean title
        if "title" in cleaned:
            cleaned["title"] = self._clean_text(cleaned["title"])
            
        # Clean company name
        if "company" in cleaned:
            cleaned["company"] = self._clean_text(cleaned["company"])
            
        # Clean location
        if "location" in cleaned:
            cleaned["location"] = self._clean_text(cleaned["location"])
            
        # Clean description
        if "description" in cleaned:
            cleaned["description"] = self._clean_text(cleaned["description"])
            
        # Clean requirements
        if "requirements" in cleaned and isinstance(cleaned["requirements"], list):
            cleaned["requirements"] = [
                self._clean_text(req) for req in cleaned["requirements"] if req
            ]
            
        # Clean salary
        if "salary" in cleaned:
            cleaned["salary"] = self._clean_salary(cleaned["salary"])
            
        # Validate required fields
        required_fields = ["title", "company", "location"]
        for field in required_fields:
            if not cleaned.get(field):
                cleaned[field] = "Unknown"
                
        return cleaned
        
    def _validate_job_quality(self, job_data: Dict[str, Any]) -> bool:
        """Validate job quality and filter out low-quality or incomplete jobs"""
        try:
            # Check if essential fields have meaningful content
            title = job_data.get("title", "").strip()
            company = job_data.get("company", "").strip()
            location = job_data.get("location", "").strip()
            description = job_data.get("description", "").strip()
            
            # Filter out jobs with missing or generic essential fields
            if not title or title.lower() in ["unknown", "n/a", "not specified", ""]:
                logger.debug(f"Filtered out job: Missing or generic title")
                return False
                
            if not company or company.lower() in ["unknown", "n/a", "not specified", ""]:
                logger.debug(f"Filtered out job: Missing or generic company")
                return False
                
            if not location or location.lower() in ["unknown", "n/a", "not specified", ""]:
                logger.debug(f"Filtered out job: Missing or generic location")
                return False
                
            # Filter out jobs with very short descriptions (likely incomplete scraping)
            if len(description) < 50:
                logger.debug(f"Filtered out job: Description too short ({len(description)} chars)")
                return False
                
            # Filter out jobs with generic/placeholder descriptions
            generic_descriptions = [
                "job description", "description coming soon", "to be updated",
                "details to be provided", "information not available", "tbd",
                "coming soon", "under review", "being updated"
            ]
            if any(generic in description.lower() for generic in generic_descriptions):
                logger.debug(f"Filtered out job: Generic description detected")
                return False
                
            # Filter out jobs with suspicious patterns (likely failed scraping)
            suspicious_patterns = [
                "error", "not found", "access denied", "forbidden", "unauthorized",
                "page not available", "content blocked", "captcha required"
            ]
            if any(pattern in description.lower() for pattern in suspicious_patterns):
                logger.debug(f"Filtered out job: Suspicious content detected")
                return False
                
            # Filter out jobs with excessive HTML/encoding artifacts
            html_artifacts = ["&nbsp;", "&amp;", "&lt;", "&gt;", "&quot;", "&#39;"]
            artifact_count = sum(description.count(artifact) for artifact in html_artifacts)
            if artifact_count > 10:  # Too many HTML artifacts suggest poor scraping
                logger.debug(f"Filtered out job: Too many HTML artifacts ({artifact_count})")
                return False
                
            # Check if the job has at least some meaningful content beyond basic fields
            meaningful_content = len(description) > 100 or job_data.get("requirements") or job_data.get("extracted_skills")
            if not meaningful_content:
                logger.debug(f"Filtered out job: Insufficient meaningful content")
                return False
                
            logger.debug(f"Job passed quality validation: {title} at {company}")
            return True
            
        except Exception as e:
            logger.error(f"Error validating job quality: {e}")
            return False
        
    def _clean_text(self, text: str) -> str:
        """Clean text data"""
        if not text:
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove HTML tags if present
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\-.,!?()]', '', text)
        
        return text
        
    def _clean_salary(self, salary: str) -> str:
        """Clean and standardize salary information"""
        if not salary:
            return ""
            
        # Remove common salary prefixes
        salary = re.sub(r'^(salary|pay|compensation):\s*', '', salary, flags=re.IGNORECASE)
        
        # Standardize currency symbols
        salary = re.sub(r'\$', 'USD ', salary)
        salary = re.sub(r'€', 'EUR ', salary)
        salary = re.sub(r'£', 'GBP ', salary)
        
        return salary.strip()
        
    async def _enrich_job_data(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich job data with additional analysis"""
        enriched = job_data.copy()
        
        # Extract skills from description
        if "description" in enriched:
            enriched["extracted_skills"] = self._extract_skills(enriched["description"])
            
        # Categorize job type
        if "title" in enriched:
            enriched["job_category"] = self._categorize_job(enriched["title"])
            
        # Estimate experience level
        if "title" in enriched or "description" in enriched:
            enriched["estimated_experience"] = self._estimate_experience_level(
                enriched.get("title", ""),
                enriched.get("description", "")
            )
            
        # Ensure all required frontend fields are present
        enriched["jobDescription"] = enriched.get("description", "")
        enriched["jobRequirements"] = enriched.get("requirements", [])
        enriched["skills"] = enriched.get("extracted_skills", [])
        enriched["rating"] = 4.5
        enriched["postedDate"] = enriched.get("posted_date", "Recently")
        
        # Preserve full description and original URL
        if "full_description" not in enriched and "description" in enriched:
            enriched["full_description"] = enriched["description"]
        if "original_url" not in enriched and "application_url" in enriched:
            enriched["original_url"] = enriched["application_url"]
            
        # Add sentiment analysis if AI is enabled
        if self.ai_enabled and "description" in enriched:
            enriched["sentiment"] = await self._analyze_sentiment(enriched["description"])
            
        return enriched
        
    def _extract_skills(self, description: str) -> List[str]:
        """Extract skills from job description"""
        skills = []
        
        # Common programming languages and technologies
        tech_skills = [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby",
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "Spring",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "SQL", "MongoDB",
            "Redis", "Elasticsearch", "Git", "Linux", "Docker", "Jenkins"
        ]
        
        description_lower = description.lower()
        for skill in tech_skills:
            if skill.lower() in description_lower:
                skills.append(skill)
                
        return skills[:10]  # Limit to top 10 skills
        
    def _categorize_job(self, title: str) -> str:
        """Categorize job based on title"""
        title_lower = title.lower()
        
        categories = {
            "Software Development": ["developer", "engineer", "programmer", "coder"],
            "Data Science": ["data scientist", "data analyst", "machine learning", "ai"],
            "DevOps": ["devops", "sre", "site reliability", "infrastructure"],
            "Design": ["designer", "ux", "ui", "graphic"],
            "Product": ["product manager", "product owner", "scrum master"],
            "Marketing": ["marketing", "growth", "seo", "content"],
            "Sales": ["sales", "account executive", "business development"],
            "Support": ["support", "customer success", "help desk"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
                
        return "Other"
        
    def _estimate_experience_level(self, title: str, description: str) -> str:
        """Estimate experience level from title and description"""
        text = f"{title} {description}".lower()
        
        # Junior level indicators
        junior_indicators = ["junior", "entry", "graduate", "intern", "0-2", "1-2", "2-3"]
        if any(indicator in text for indicator in junior_indicators):
            return "Junior"
            
        # Senior level indicators
        senior_indicators = ["senior", "lead", "principal", "architect", "5+", "7+", "10+"]
        if any(indicator in text for indicator in senior_indicators):
            return "Senior"
            
        # Mid level indicators
        mid_indicators = ["mid", "intermediate", "3-5", "4-6", "5-7"]
        if any(indicator in text for indicator in mid_indicators):
            return "Mid-level"
            
        return "Unknown"
        
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of job description using AI"""
        # TODO: Implement AI-powered sentiment analysis
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "keywords": []
        }
        
    async def cleanup(self):
        """Cleanup processor resources"""
        if self.ai_client:
            # TODO: Cleanup AI client
            pass
        logger.info("Job processor cleaned up")

