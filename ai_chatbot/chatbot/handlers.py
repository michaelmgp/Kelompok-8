
from pydantic import BaseModel, Field
from typing import List, Optional
from .model import get_llm
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)

class Filters(BaseModel):
    skills: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    rate_type: Optional[str] = Field(default=None, description="fixed, hourly, monthly, or null")
    remote: Optional[bool] = None
    duration_days_max: Optional[int] = None
    top_k: int = 5

class ChatResult(BaseModel):
    message: str
    filters: Filters
    should_fetch_jobs: bool = True

FILTER_PROMPT = """
Convert the user's natural-language job request into a STRICT JSON object:

{
  "skills": [str],
  "keywords": [str],
  "budget_min": int|null,
  "budget_max": int|null,
  "rate_type": "fixed"|"hourly"|"monthly"|null,
  "remote": true|false|null,
  "duration_days_max": int|null,
  "top_k": int
}

Rules:
- Output ONLY valid JSON (no prose, no code fences).
- Normalize skills/keywords to lowercase.
- Money like "$1000" or ">$30/hour" or "1500USD/month": map to budget_* and set rate_type.
- "remote" => remote=true. "fulltime" => duration_days_max ≈ 365. "< 1 month" => duration_days_max ≈ 30.
- Extract skills from job titles (e.g., "Java developer" => skills: ["java", "developer"])

User:
"""{user_prompt}"""
"""

SUMMARY_PROMPT = """
Write a brief, friendly message in English explaining what you will search for,
based on the filters below (JSON). Keep it to 2–3 sentences. Do NOT list jobs.

{filters_json}
"""

def _strip_code_fences(s: str) -> str:
    t = s.strip()
    if t.startswith("```"):
        t = t.strip("` \n\r\t")
        if t.lower().startswith("json"):
            t = t[4:].strip()
    return t

def _extract_fallback_filters(user_prompt: str) -> dict:
    """Extract basic filters when Grok parsing fails"""
    prompt_lower = user_prompt.lower()
    
    # Extract skills
    skills = []
    if "java" in prompt_lower:
        skills.append("java")
    if "python" in prompt_lower:
        skills.append("python")
    if "react" in prompt_lower:
        skills.append("react")
    if "javascript" in prompt_lower or "js" in prompt_lower:
        skills.append("javascript")
    if "typescript" in prompt_lower or "ts" in prompt_lower:
        skills.append("typescript")
    if "node" in prompt_lower:
        skills.append("node.js")
    if "angular" in prompt_lower:
        skills.append("angular")
    if "vue" in prompt_lower:
        skills.append("vue")
    if "blockchain" in prompt_lower:
        skills.append("blockchain")
    if "ai" in prompt_lower or "ml" in prompt_lower or "machine learning" in prompt_lower:
        skills.append("ai/ml")
    if "devops" in prompt_lower:
        skills.append("devops")
    if "docker" in prompt_lower:
        skills.append("docker")
    if "kubernetes" in prompt_lower or "k8s" in prompt_lower:
        skills.append("kubernetes")
    if "aws" in prompt_lower or "amazon" in prompt_lower:
        skills.append("aws")
    if "azure" in prompt_lower:
        skills.append("azure")
    if "gcp" in prompt_lower or "google cloud" in prompt_lower:
        skills.append("gcp")
    
    # Extract keywords
    keywords = []
    if "developer" in prompt_lower:
        keywords.append("developer")
    if "engineer" in prompt_lower:
        keywords.append("engineer")
    if "job" in prompt_lower or "jobs" in prompt_lower:
        keywords.append("job")
    
    # Extract salary information
    budget_min = None
    budget_max = None
    rate_type = None
    
    import re
    # Look for salary patterns
    salary_patterns = [
        r'(\d+)\s*usd?\s*a\s*month',     # 1500USD a month
        r'(\d+)\s*usd?\s*per\s*month',   # 1500USD per month
        r'(\d+)\s*usd?/?month',          # 1500USD/month
        r'(\d+)\s*usd?/?hour',           # 50USD/hour
        r'\$(\d+)',                      # $1500
        r'(\d+)\s*per\s*hour',          # 50 per hour
        r'(\d+)\s*per\s*month',         # 1500 per month
        r'minimum\s*(\d+)\s*usd?\s*a\s*month',  # minimum 1500USD a month
        r'minimum\s*(\d+)\s*usd?\s*per\s*month', # minimum 1500USD per month
        r'minimum\s*\$(\d+)',            # minimum $1500
    ]
    
    for pattern in salary_patterns:
        match = re.search(pattern, prompt_lower)
        if match:
            amount = int(match.group(1))
            if "hour" in pattern or "per hour" in prompt_lower:
                rate_type = "hourly"
                budget_min = amount
                budget_max = amount + 50  # Add some range
            elif "month" in pattern or "per month" in prompt_lower or "a month" in prompt_lower:
                rate_type = "monthly"
                budget_min = amount
                budget_max = amount + 500  # Add some range
            else:
                rate_type = "fixed"
                budget_min = amount
                budget_max = amount + 1000  # Add some range
            break
    
    # Extract remote preference
    remote = None
    if "remote" in prompt_lower:
        remote = True
    
    # Extract duration/employment type
    duration_days_max = None
    if "fulltime" in prompt_lower or "full time" in prompt_lower:
        duration_days_max = 365  # Full time job
    elif "part time" in prompt_lower or "parttime" in prompt_lower:
        duration_days_max = 180  # Part time job
    elif "contract" in prompt_lower:
        duration_days_max = 90   # Contract job
    
    # Extract number of jobs requested
    top_k = 5  # default
    job_count_patterns = [
        r'give\s+me\s+(\d+)\s+jobs?',
        r'(\d+)\s+jobs?',
        r'(\d+)\s+positions?',
        r'(\d+)\s+opportunities?'
    ]
    
    for pattern in job_count_patterns:
        match = re.search(pattern, prompt_lower)
        if match:
            count = int(match.group(1))
            top_k = max(1, min(count, 20))  # Limit to 1-20
            break
    
    return {
        "skills": skills,
        "keywords": keywords,
        "budget_min": budget_min,
        "budget_max": budget_max,
        "rate_type": rate_type,
        "remote": remote,
        "duration_days_max": duration_days_max,
        "top_k": top_k
    }

def parse_filters(user_prompt: str) -> Filters:
    logger.info(f"🔍 Parsing user prompt: {user_prompt}")
    
    llm = get_llm()
    logger.info("🤖 Sending prompt to Grok for filter parsing...")
    
    raw = llm.invoke(FILTER_PROMPT.format(user_prompt=user_prompt)).content or ""
    logger.info(f"📝 Grok raw response for filters: {raw}")
    
    raw = _strip_code_fences(raw)
    logger.info(f"🧹 Cleaned response: {raw}")
    
    js = None
    try:
        js = json.loads(raw)
        logger.info(f"✅ Successfully parsed JSON filters: {json.dumps(js, indent=2)}")
    except Exception as e:
        logger.error(f"❌ JSON parsing failed: {e}")
        logger.info("🔄 Attempting fallback filter extraction...")
        js = _extract_fallback_filters(user_prompt)
        logger.info(f"🔄 Fallback filters extracted: {json.dumps(js, indent=2)}")
    
    # Validate and normalize the filters
    if js.get("rate_type") not in (None, "fixed", "hourly", "monthly"):
        js["rate_type"] = None
        logger.info("🔄 Reset invalid rate_type to None")
    
    try:
        tk = int(js.get("top_k", 5))
        js["top_k"] = max(1, min(tk, 20))
        logger.info(f"📊 Set top_k to: {js['top_k']}")
    except Exception:
        js["top_k"] = 5
        logger.info("🔄 Set top_k to default: 5")
    
    # Ensure required fields exist
    if "skills" not in js:
        js["skills"] = []
    if "keywords" not in js:
        js["keywords"] = []
    
    filters = Filters(**js)
    logger.info(f"🎯 Final parsed filters: {filters.model_dump_json(indent=2)}")
    return filters

def build_reply(filters: Filters) -> str:
    logger.info("🤖 Building reply message with Grok...")
    
    llm = get_llm()
    response = llm.invoke(SUMMARY_PROMPT.format(filters_json=filters.model_dump_json()))
    
    message = response.content or ""
    logger.info(f"📝 Grok generated reply: {message}")
    
    return message

def handle_chat(user_prompt: str) -> ChatResult:
    logger.info("=" * 60)
    logger.info(f"💬 NEW CHAT REQUEST: {user_prompt}")
    logger.info("=" * 60)
    
    filters = parse_filters(user_prompt)
    message = build_reply(filters)
    
    result = ChatResult(message=message, filters=filters)
    logger.info(f"✅ Chat result created: {result.model_dump_json(indent=2)}")
    logger.info("=" * 60)
    
    return result
