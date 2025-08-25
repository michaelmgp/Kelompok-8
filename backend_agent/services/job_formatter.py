import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from collections import defaultdict, Counter
import re

from agents.coordinator import UnifiedJob

logger = logging.getLogger(__name__)

@dataclass
class JobAnalytics:
    """Analytics data for job analysis"""
    total_jobs: int
    platform_breakdown: Dict[str, int]
    category_breakdown: Dict[str, int]
    skill_frequency: Dict[str, int]
    budget_analysis: Dict[str, Any]
    time_analysis: Dict[str, Any]
    ai_score_distribution: Dict[str, int]

@dataclass
class FormattedJob:
    """Formatted job for display"""
    id: str
    title: str
    description: str
    budget: Optional[str]
    skills: List[str]
    category: str
    platform: str
    posted_date: str
    url: str
    ai_score: float
    highlights: List[str]
    platform_badge: str

class JobFormatter:
    """
    Formats and analyzes job data for presentation and analytics
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.skill_keywords = self._load_skill_keywords()
        self.category_mappings = self._load_category_mappings()
        
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """Load skill keywords for categorization"""
        return {
            "programming": [
                "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust",
                "swift", "kotlin", "typescript", "react", "angular", "vue", "node.js",
                "django", "flask", "spring", "laravel", "express", "asp.net"
            ],
            "design": [
                "ui/ux", "graphic design", "web design", "logo design", "illustration",
                "photoshop", "illustrator", "figma", "sketch", "invision", "prototyping"
            ],
            "marketing": [
                "seo", "sem", "social media", "content marketing", "email marketing",
                "ppc", "google ads", "facebook ads", "influencer marketing", "analytics"
            ],
            "writing": [
                "content writing", "copywriting", "blog writing", "technical writing",
                "creative writing", "editing", "proofreading", "translation"
            ],
            "data": [
                "data analysis", "machine learning", "ai", "data science", "statistics",
                "sql", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn"
            ]
        }
    
    def _load_category_mappings(self) -> Dict[str, str]:
        """Load category mappings for standardization"""
        return {
            "web development": "development",
            "mobile development": "development",
            "software development": "development",
            "web design": "design",
            "graphic design": "design",
            "digital marketing": "marketing",
            "social media marketing": "marketing",
            "content creation": "writing",
            "data entry": "data",
            "data processing": "data"
        }
    
    def format_jobs_for_display(
        self, 
        jobs: List[UnifiedJob], 
        format_type: str = "standard"
    ) -> List[FormattedJob]:
        """
        Format jobs for display with different presentation styles
        """
        formatted_jobs = []
        
        for job in jobs:
            formatted_job = self._format_single_job(job, format_type)
            formatted_jobs.append(formatted_job)
        
        return formatted_jobs
    
    def _format_single_job(self, job: UnifiedJob, format_type: str) -> FormattedJob:
        """Format a single job"""
        # Standardize category
        category = self._standardize_category(job.category)
        
        # Extract highlights
        highlights = self._extract_job_highlights(job)
        
        # Create platform badge
        platform_badge = self._create_platform_badge(job.platform)
        
        # Format description based on type
        description = self._format_description(job.description, format_type)
        
        # Format budget
        budget = self._format_budget(job.budget)
        
        # Format date
        posted_date = self._format_date(job.posted_date)
        
        return FormattedJob(
            id=job.id,
            title=job.title,
            description=description,
            budget=budget,
            skills=job.skills,
            category=category,
            platform=job.platform,
            posted_date=posted_date,
            url=job.url,
            ai_score=job.ai_score,
            highlights=highlights,
            platform_badge=platform_badge
        )
    
    def _standardize_category(self, category: str) -> str:
        """Standardize job category"""
        if not category:
            return "general"
        
        category_lower = category.lower().strip()
        
        # Check direct mappings
        if category_lower in self.category_mappings:
            return self.category_mappings[category_lower]
        
        # Check keyword matches
        for standard_category, keywords in self.skill_keywords.items():
            if any(keyword in category_lower for keyword in keywords):
                return standard_category
        
        return category_lower
    
    def _extract_job_highlights(self, job: UnifiedJob) -> List[str]:
        """Extract key highlights from job data"""
        highlights = []
        
        # Budget highlights
        if job.budget:
            try:
                budget_amount = float(job.budget.replace("$", "").replace(",", ""))
                if budget_amount > 1000:
                    highlights.append("High Budget")
                elif budget_amount > 500:
                    highlights.append("Medium Budget")
            except:
                pass
        
        # Skills highlights
        if job.skills:
            if len(job.skills) >= 5:
                highlights.append("Multiple Skills")
            elif len(job.skills) >= 3:
                highlights.append("Skill Variety")
        
        # AI score highlights
        if job.ai_score >= 0.8:
            highlights.append("Top Match")
        elif job.ai_score >= 0.6:
            highlights.append("Good Match")
        
        # Platform-specific highlights
        if job.platform == "upwork":
            client_info = job.platform_specific_data.get("client_info", {})
            if client_info.get("total_spent"):
                try:
                    total_spent = float(client_info["total_spent"])
                    if total_spent > 10000:
                        highlights.append("Established Client")
                    elif total_spent > 5000:
                        highlights.append("Active Client")
                except:
                    pass
        
        elif job.platform == "fiverr":
            seller_info = job.platform_specific_data.get("seller_info", {})
            if seller_info.get("level") == "Top Rated":
                highlights.append("Top Rated Seller")
            elif seller_info.get("rating") and seller_info["rating"] >= 4.8:
                highlights.append("High Rating")
        
        return highlights[:3]  # Limit to 3 highlights
    
    def _create_platform_badge(self, platform: str) -> str:
        """Create a platform badge"""
        badges = {
            "upwork": "🔵 Upwork",
            "fiverr": "🟢 Fiverr"
        }
        return badges.get(platform, platform.title())
    
    def _format_description(self, description: str, format_type: str) -> str:
        """Format job description"""
        if not description:
            return ""
        
        # Clean description
        clean_desc = re.sub(r'\s+', ' ', description.strip())
        
        if format_type == "compact":
            # Truncate for compact view
            if len(clean_desc) > 150:
                return clean_desc[:150] + "..."
        elif format_type == "detailed":
            # Keep full description
            return clean_desc
        else:
            # Standard format - truncate at 200 chars
            if len(clean_desc) > 200:
                return clean_desc[:200] + "..."
        
        return clean_desc
    
    def _format_budget(self, budget: Optional[str]) -> Optional[str]:
        """Format budget display"""
        if not budget:
            return None
        
        # Clean and standardize budget format
        budget_clean = budget.strip()
        
        # Add currency symbol if missing
        if not budget_clean.startswith('$'):
            budget_clean = f"${budget_clean}"
        
        return budget_clean
    
    def _format_date(self, date: datetime) -> str:
        """Format posted date"""
        now = datetime.utcnow()
        time_diff = now - date
        
        if time_diff.days == 0:
            if time_diff.seconds < 3600:
                minutes = time_diff.seconds // 60
                return f"{minutes}m ago"
            else:
                hours = time_diff.seconds // 3600
                return f"{hours}h ago"
        elif time_diff.days == 1:
            return "1 day ago"
        elif time_diff.days < 7:
            return f"{time_diff.days} days ago"
        else:
            return date.strftime("%b %d")
    
    def analyze_jobs(self, jobs: List[UnifiedJob]) -> JobAnalytics:
        """
        Generate comprehensive analytics for job data
        """
        if not jobs:
            return JobAnalytics(
                total_jobs=0,
                platform_breakdown={},
                category_breakdown={},
                skill_frequency={},
                budget_analysis={},
                time_analysis={},
                ai_score_distribution={}
            )
        
        # Platform breakdown
        platform_counts = Counter(job.platform for job in jobs)
        
        # Category breakdown
        category_counts = Counter()
        for job in jobs:
            category = self._standardize_category(job.category)
            category_counts[category] += 1
        
        # Skill frequency
        skill_counts = Counter()
        for job in jobs:
            for skill in job.skills:
                skill_counts[skill.lower()] += 1
        
        # Budget analysis
        budget_data = self._analyze_budgets(jobs)
        
        # Time analysis
        time_data = self._analyze_time_patterns(jobs)
        
        # AI score distribution
        score_distribution = self._analyze_ai_scores(jobs)
        
        return JobAnalytics(
            total_jobs=len(jobs),
            platform_breakdown=dict(platform_counts),
            category_breakdown=dict(category_counts),
            skill_frequency=dict(skill_counts.most_common(20)),
            budget_analysis=budget_data,
            time_analysis=time_data,
            ai_score_distribution=score_distribution
        )
    
    def _analyze_budgets(self, jobs: List[UnifiedJob]) -> Dict[str, Any]:
        """Analyze budget patterns"""
        budgets = []
        
        for job in jobs:
            if job.budget:
                try:
                    budget_amount = float(job.budget.replace("$", "").replace(",", ""))
                    budgets.append(budget_amount)
                except:
                    continue
        
        if not budgets:
            return {
                "average": 0,
                "median": 0,
                "min": 0,
                "max": 0,
                "distribution": {}
            }
        
        budgets.sort()
        avg_budget = sum(budgets) / len(budgets)
        median_budget = budgets[len(budgets) // 2]
        
        # Budget distribution
        distribution = {
            "Under $100": len([b for b in budgets if b < 100]),
            "$100-$500": len([b for b in budgets if 100 <= b < 500]),
            "$500-$1000": len([b for b in budgets if 500 <= b < 1000]),
            "$1000-$5000": len([b for b in budgets if 1000 <= b < 5000]),
            "Over $5000": len([b for b in budgets if b >= 5000])
        }
        
        return {
            "average": round(avg_budget, 2),
            "median": median_budget,
            "min": min(budgets),
            "max": max(budgets),
            "distribution": distribution
        }
    
    def _analyze_time_patterns(self, jobs: List[UnifiedJob]) -> Dict[str, Any]:
        """Analyze time-based patterns"""
        now = datetime.utcnow()
        
        # Group by time periods
        time_periods = {
            "Last hour": 0,
            "Last 24 hours": 0,
            "Last 7 days": 0,
            "Last 30 days": 0,
            "Older": 0
        }
        
        for job in jobs:
            time_diff = now - job.posted_date
            
            if time_diff.total_seconds() < 3600:
                time_periods["Last hour"] += 1
            elif time_diff.days == 0:
                time_periods["Last 24 hours"] += 1
            elif time_diff.days < 7:
                time_periods["Last 7 days"] += 1
            elif time_diff.days < 30:
                time_periods["Last 30 days"] += 1
            else:
                time_periods["Older"] += 1
        
        return time_periods
    
    def _analyze_ai_scores(self, jobs: List[UnifiedJob]) -> Dict[str, int]:
        """Analyze AI score distribution"""
        score_ranges = {
            "0.0-0.2": 0,
            "0.2-0.4": 0,
            "0.4-0.6": 0,
            "0.6-0.8": 0,
            "0.8-1.0": 0
        }
        
        for job in jobs:
            score = job.ai_score
            
            if score < 0.2:
                score_ranges["0.0-0.2"] += 1
            elif score < 0.4:
                score_ranges["0.2-0.4"] += 1
            elif score < 0.6:
                score_ranges["0.4-0.6"] += 1
            elif score < 0.8:
                score_ranges["0.6-0.8"] += 1
            else:
                score_ranges["0.8-1.0"] += 1
        
        return score_ranges
    
    def generate_job_recommendations(
        self, 
        user_profile: Dict[str, Any], 
        available_jobs: List[UnifiedJob]
    ) -> List[UnifiedJob]:
        """
        Generate personalized job recommendations based on user profile
        """
        if not available_jobs or not user_profile:
            return []
        
        # Score jobs based on user preferences
        scored_jobs = []
        
        for job in available_jobs:
            score = self._calculate_personalization_score(job, user_profile)
            scored_jobs.append((job, score))
        
        # Sort by personalization score
        scored_jobs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top recommendations
        return [job for job, score in scored_jobs[:20]]
    
    def _calculate_personalization_score(
        self, 
        job: UnifiedJob, 
        user_profile: Dict[str, Any]
    ) -> float:
        """Calculate personalization score for a job"""
        score = 0.0
        
        # Skills match
        user_skills = set(skill.lower() for skill in user_profile.get("skills", []))
        job_skills = set(skill.lower() for skill in job.skills)
        
        if user_skills and job_skills:
            skill_overlap = len(user_skills.intersection(job_skills))
            skill_score = skill_overlap / len(user_skills)
            score += skill_score * 0.4
        
        # Platform preference
        preferred_platforms = user_profile.get("preferred_platforms", [])
        if job.platform in preferred_platforms:
            score += 0.2
        
        # Experience level match
        user_experience = user_profile.get("experience_level", "").lower()
        if user_experience in ["beginner", "entry"] and job.ai_score < 0.5:
            score += 0.1
        elif user_experience in ["intermediate", "mid"] and 0.3 <= job.ai_score <= 0.7:
            score += 0.1
        elif user_experience in ["expert", "senior"] and job.ai_score > 0.6:
            score += 0.1
        
        # AI score boost
        score += job.ai_score * 0.3
        
        return min(score, 1.0)
    
    def export_jobs_data(
        self, 
        jobs: List[UnifiedJob], 
        format: str = "json"
    ) -> str:
        """
        Export jobs data in various formats
        """
        if format == "json":
            return json.dumps(
                [self._job_to_dict(job) for job in jobs],
                indent=2,
                default=str
            )
        elif format == "csv":
            return self._jobs_to_csv(jobs)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _job_to_dict(self, job: UnifiedJob) -> Dict[str, Any]:
        """Convert job to dictionary for export"""
        return {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "budget": job.budget,
            "skills": job.skills,
            "category": job.category,
            "platform": job.platform,
            "posted_date": job.posted_date.isoformat(),
            "url": job.url,
            "ai_score": job.ai_score,
            "created_at": job.created_at.isoformat()
        }
    
    def _jobs_to_csv(self, jobs: List[UnifiedJob]) -> str:
        """Convert jobs to CSV format"""
        if not jobs:
            return ""
        
        # Get headers from first job
        headers = list(self._job_to_dict(jobs[0]).keys())
        
        # Create CSV
        csv_lines = [",".join(headers)]
        
        for job in jobs:
            job_dict = self._job_to_dict(job)
            row = [str(job_dict[header]) for header in headers]
            csv_lines.append(",".join(row))
        
        return "\n".join(csv_lines) 