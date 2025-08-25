
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .model import get_llm
from .icp_integration import ICPIntegration, PersonalizedChatbot
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
    personalized: bool = False
    user_profile: Optional[Dict[str, Any]] = None
    reputation_score: Optional[float] = None

class ChatRequest(BaseModel):
    user_prompt: str
    top_k: int = 5
    user_principal: Optional[str] = None  # ICP user principal for personalization

# Global ICP integration (will be initialized in main.py)
icp_integration: Optional[ICPIntegration] = None
personalized_chatbot: Optional[PersonalizedChatbot] = None

def set_icp_integration(integration: ICPIntegration):
    """Set the ICP integration instance"""
    global icp_integration, personalized_chatbot
    icp_integration = integration
    personalized_chatbot = PersonalizedChatbot(integration)
    logger.info("🔗 ICP integration initialized")

FILTER_PROMPT = """
Convert the user's natural-language job request into a STRICT JSON object:

{{
  "skills": [str],
  "keywords": [str],
  "budget_min": int|null,
  "budget_max": int|null,
  "rate_type": "fixed"|"hourly"|"monthly"|null,
  "remote": true|false|null,
  "duration_days_max": int|null,
  "top_k": int
}}

Rules:
- Output ONLY valid JSON (no prose, no code fences).
- Normalize skills/keywords to lowercase.
- Money like "$1000" or ">$30/hour" or "1500USD/month": map to budget_* and set rate_type.
- "remote" => remote=true. "fulltime" => duration_days_max ≈ 365. "< 1 month" => duration_days_max ≈ 30.
- Extract skills from job titles (e.g., "Java developer" => skills: ["java", "developer"])

User:
\"\"\"{user_prompt}\"\"\"
"""

PERSONALIZED_FILTER_PROMPT = """
Based on the user's profile and request, create a STRICT JSON object for job search:

User Profile Context:
{user_context}

User Request: {user_prompt}

Create JSON with enhanced filters considering the user's:
- Skills and experience level
- Location preferences  
- Reputation and verification status
- Previous job patterns

Output ONLY valid JSON:
{{
  "skills": [str],
  "keywords": [str],
  "budget_min": int|null,
  "budget_max": int|null,
  "rate_type": "fixed"|"hourly"|"monthly"|null,
  "remote": true|false|null,
  "duration_days_max": int|null,
  "top_k": int
}}
"""

SUMMARY_PROMPT = """
Write a brief, friendly message in English explaining what you will search for,
based on the filters below (JSON). Keep it to 2–3 sentences. Do NOT list jobs.

{filters_json}
"""

PERSONALIZED_SUMMARY_PROMPT = """
Based on the user's profile and preferences, write a personalized message explaining what you will search for.

User Profile:
{user_profile}

Filters: {filters_json}

Write a friendly, personalized response (2-3 sentences) that:
- Acknowledges their experience level and skills
- Mentions their location preferences
- References their reputation/verification status
- Explains the enhanced search criteria
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

async def parse_filters_with_profile(user_prompt: str, user_profile: Dict[str, Any]) -> Filters:
    """Parse filters with user profile context for personalization"""
    logger.info(f"🔍 Parsing filters with user profile: {user_profile.get('name', 'Unknown')}")
    
    llm = get_llm()
    logger.info("🤖 Sending personalized prompt to Grok for filter parsing...")
    
    # Create personalized prompt
    user_context = f"""
    Name: {user_profile.get('name', 'Unknown')}
    Experience: {user_profile.get('experience_level', 'Unknown')}
    Location: {user_profile.get('location', 'Unknown')}
    Skills: {', '.join(user_profile.get('skills', []))}
    Reputation: {user_profile.get('reputation_score', 0.0)}/5.0
    Verification: {user_profile.get('verification_status', 'Unknown')}
    """
    
    personalized_prompt = PERSONALIZED_FILTER_PROMPT.format(
        user_context=user_context,
        user_prompt=user_prompt
    )
    
    raw = llm.invoke(personalized_prompt).content or ""
    logger.info(f"📝 Grok personalized response: {raw}")
    
    raw = _strip_code_fences(raw)
    logger.info(f"🧹 Cleaned personalized response: {raw}")
    
    js = None
    try:
        js = json.loads(raw)
        logger.info(f"✅ Successfully parsed personalized JSON filters: {json.dumps(js, indent=2)}")
    except Exception as e:
        logger.error(f"❌ Personalized JSON parsing failed: {e}")
        logger.info("🔄 Using fallback filter extraction...")
        js = _extract_fallback_filters(user_prompt)
        logger.info(f"🔄 Fallback filters extracted: {json.dumps(js, indent=2)}")
    
    # Enhance filters with user profile
    if personalized_chatbot and user_profile:
        js = personalized_chatbot.enhance_filters_with_profile(js, user_profile)
    
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
    logger.info(f"🎯 Final personalized filters: {filters.model_dump_json(indent=2)}")
    return filters

def parse_filters(user_prompt: str) -> Filters:
    """Standard filter parsing without personalization"""
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

def build_reply(filters: Filters, user_profile: Optional[Dict[str, Any]] = None) -> str:
    """Build reply message with optional personalization"""
    logger.info("🤖 Building reply message with Grok...")
    
    llm = get_llm()
    
    if user_profile:
        # Personalized reply
        user_context = f"""
        Name: {user_profile.get('name', 'Unknown')}
        Experience: {user_profile.get('experience_level', 'Unknown')}
        Skills: {', '.join(user_profile.get('skills', []))}
        """
        
        prompt = PERSONALIZED_SUMMARY_PROMPT.format(
            user_profile=user_context,
            filters_json=filters.model_dump_json()
        )
    else:
        # Standard reply
        prompt = SUMMARY_PROMPT.format(filters_json=filters.model_dump_json())
    
    response = llm.invoke(prompt)
    message = response.content or ""
    logger.info(f"📝 Grok generated {'personalized ' if user_profile else ''}reply: {message}")
    
    return message

async def handle_chat_with_profile(user_prompt: str, user_principal: str) -> ChatResult:
    """Handle chat with ICP user profile integration"""
    logger.info("=" * 60)
    logger.info(f"💬 PERSONALIZED CHAT REQUEST: {user_prompt}")
    logger.info(f"👤 User Principal: {user_principal}")
    logger.info("=" * 60)
    
    try:
        # Get personalized response from ICP
        if personalized_chatbot:
            personalization_result = await personalized_chatbot.get_personalized_response(user_principal, user_prompt)
            
            if personalization_result.get("personalized"):
                user_profile = personalization_result["user_profile"]
                logger.info(f"🎯 Using personalized filters for {user_profile.name}")
                
                # Parse filters with profile context
                filters = await parse_filters_with_profile(user_prompt, user_profile)
                
                # Build personalized reply
                message = build_reply(filters, user_profile)
                
                result = ChatResult(
                    message=message,
                    filters=filters,
                    personalized=True,
                    user_profile=user_profile.__dict__,
                    reputation_score=user_profile.reputation_score
                )
                
                logger.info(f"✅ Personalized chat result created: {result.model_dump_json(indent=2)}")
                return result
            else:
                logger.info("🔄 Falling back to standard processing")
        
        # Fallback to standard processing
        filters = parse_filters(user_prompt)
        message = build_reply(filters)
        
        result = ChatResult(
            message=message,
            filters=filters,
            personalized=False
        )
        
        logger.info(f"✅ Standard chat result created: {result.model_dump_json(indent=2)}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in personalized chat: {e}")
        # Fallback to standard processing
        filters = parse_filters(user_prompt)
        message = build_reply(filters)
        
        result = ChatResult(
            message=message,
            filters=filters,
            personalized=False
        )
        
        return result
    
    finally:
        logger.info("=" * 60)

def handle_chat(user_prompt: str) -> ChatResult:
    """Standard chat handling without personalization"""
    logger.info("=" * 60)
    logger.info(f"💬 NEW CHAT REQUEST: {user_prompt}")
    logger.info("=" * 60)
    
    filters = parse_filters(user_prompt)
    message = build_reply(filters)
    
    result = ChatResult(message=message, filters=filters, personalized=False)
    logger.info(f"✅ Chat result created: {result.model_dump_json(indent=2)}")
    logger.info("=" * 60)
    
    return result
