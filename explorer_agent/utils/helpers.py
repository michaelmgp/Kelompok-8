"""
Helper utility functions for the Explorer Agent

Common utilities used across the system
"""

import re
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text data"""
    if not text:
        return ""
        
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?()]', '', text)
    
    return text.strip()

def extract_salary_range(text: str) -> Dict[str, Any]:
    """Extract salary information from text"""
    if not text:
        return {}
        
    # Common salary patterns
    patterns = [
        r'(\$[\d,]+)\s*-\s*(\$[\d,]+)',  # $50,000 - $80,000
        r'(\$[\d,]+)\s*to\s*(\$[\d,]+)',  # $50,000 to $80,000
        r'(\$[\d,]+)\s*per\s*(year|month|hour)',  # $50,000 per year
        r'(\$[\d,]+)',  # Single amount
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                min_salary = match.group(1).replace(',', '')
                max_salary = match.group(2).replace(',', '')
                return {
                    "min": float(min_salary.replace('$', '')),
                    "max": float(max_salary.replace('$', '')),
                    "currency": "USD"
                }
            elif len(match.groups()) == 1:
                amount = match.group(1).replace(',', '')
                return {
                    "amount": float(amount.replace('$', '')),
                    "currency": "USD"
                }
                
    return {}

def parse_location(location_text: str) -> Dict[str, str]:
    """Parse location text into structured components"""
    if not location_text:
        return {}
        
    # Common location patterns
    patterns = [
        r'^([^,]+),\s*([^,]+),\s*([^,]+)$',  # City, State, Country
        r'^([^,]+),\s*([^,]+)$',  # City, State/Country
        r'^([^,]+)$',  # Single location
    ]
    
    for pattern in patterns:
        match = re.search(pattern, location_text.strip())
        if match:
            groups = match.groups()
            if len(groups) == 3:
                return {
                    "city": groups[0].strip(),
                    "state": groups[1].strip(),
                    "country": groups[2].strip()
                }
            elif len(groups) == 2:
                return {
                    "city": groups[0].strip(),
                    "state": groups[1].strip()
                }
            elif len(groups) == 1:
                return {
                    "city": groups[0].strip()
                }
                
    return {"raw": location_text}

def extract_skills_from_text(text: str, skill_list: List[str] = None) -> List[str]:
    """Extract skills from text using a predefined skill list"""
    if not text:
        return []
        
    if not skill_list:
        # Default tech skills
        skill_list = [
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby",
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "Spring",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP", "SQL", "MongoDB",
            "Redis", "Elasticsearch", "Git", "Linux", "Jenkins", "Ansible"
        ]
        
    found_skills = []
    text_lower = text.lower()
    
    for skill in skill_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)
            
    return found_skills[:10]  # Limit to top 10 skills

def estimate_experience_level(title: str, description: str) -> str:
    """Estimate experience level from job title and description"""
    text = f"{title} {description}".lower()
    
    # Junior level indicators
    junior_indicators = [
        "junior", "entry", "graduate", "intern", "0-2", "1-2", "2-3",
        "associate", "trainee", "apprentice"
    ]
    
    # Senior level indicators
    senior_indicators = [
        "senior", "lead", "principal", "architect", "5+", "7+", "10+",
        "staff", "director", "manager"
    ]
    
    # Mid level indicators
    mid_indicators = [
        "mid", "intermediate", "3-5", "4-6", "5-7", "mid-level"
    ]
    
    if any(indicator in text for indicator in senior_indicators):
        return "Senior"
    elif any(indicator in text for indicator in mid_indicators):
        return "Mid-level"
    elif any(indicator in text for indicator in junior_indicators):
        return "Junior"
    else:
        return "Unknown"

def categorize_job(title: str) -> str:
    """Categorize job based on title"""
    title_lower = title.lower()
    
    categories = {
        "Software Development": ["developer", "engineer", "programmer", "coder", "software"],
        "Data Science": ["data scientist", "data analyst", "machine learning", "ai", "ml engineer"],
        "DevOps": ["devops", "sre", "site reliability", "infrastructure", "platform"],
        "Design": ["designer", "ux", "ui", "graphic", "visual"],
        "Product": ["product manager", "product owner", "scrum master", "agile"],
        "Marketing": ["marketing", "growth", "seo", "content", "digital marketing"],
        "Sales": ["sales", "account executive", "business development", "sales manager"],
        "Support": ["support", "customer success", "help desk", "technical support"]
    }
    
    for category, keywords in categories.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
            
    return "Other"

def build_search_url(base_url: str, params: Dict[str, Any]) -> str:
    """Build search URL with query parameters"""
    if not params:
        return base_url
        
    query_parts = []
    for key, value in params.items():
        if value:
            if isinstance(value, bool):
                if value:
                    query_parts.append(f"{key}=true")
            else:
                query_parts.append(f"{key}={value}")
                
    if query_parts:
        return f"{base_url}?{'&'.join(query_parts)}"
    return base_url

def validate_url(url: str) -> bool:
    """Validate if a string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return ""

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and dots
    filename = re.sub(r'\s+', '_', filename.strip())
    filename = filename.strip('.')
    return filename

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split a list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def retry_with_backoff(func, max_retries: int = 3, base_delay: float = 1.0):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
            import time
            time.sleep(delay)

