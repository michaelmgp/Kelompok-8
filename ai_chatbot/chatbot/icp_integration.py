"""
ICP Integration Module for AI Chatbot
Integrates with ICP identity and chat contracts for personalized responses
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Try to import ic_agent, but provide fallback if not available
try:
    from ic_agent import Agent, Identity, Principal
    from ic_agent.agent import AgentError
    ICP_AGENT_AVAILABLE = True
    logger.info("✅ ic_agent library available")
except ImportError:
    ICP_AGENT_AVAILABLE = False
    logger.warning("⚠️ ic_agent library not available, using mock mode")
    
    # Create mock classes for fallback
    class Agent:
        pass
    
    class Identity:
        pass
    
    class Principal:
        pass
    
    class AgentError(Exception):
        pass

@dataclass
class UserProfile:
    """User profile from ICP identity contract"""
    principal: str
    name: str
    email: str
    bio: str
    skills: List[str]
    portfolio_url: str
    location: str
    experience_level: str
    verification_status: str
    reputation_score: float
    created_at: int
    updated_at: int

@dataclass
class ChatRecord:
    """Chat record for ICP chat contract"""
    id: int
    user: str
    message: str
    timestamp: int

class ICPIntegration:
    """Handles integration with ICP canisters"""
    
    def __init__(self, identity_canister_id: str, chat_canister_id: str, agent: Optional[Agent] = None):
        self.identity_canister_id = identity_canister_id
        self.chat_canister_id = chat_canister_id
        self.agent = agent
        
        # Check if we're in mock mode
        if identity_canister_id == "mock" or chat_canister_id == "mock":
            logger.info("🤖 Running in mock mode - no real ICP connection")
            self.mock_mode = True
        else:
            self.mock_mode = False
            
    async def get_user_profile(self, user_principal: str) -> Optional[UserProfile]:
        """Get user profile from ICP identity contract"""
        try:
            logger.info(f"🔍 Fetching user profile for principal: {user_principal}")
            
            if self.mock_mode:
                # Return mock profile for testing
                mock_profile = UserProfile(
                    principal=user_principal,
                    name="Mock User",
                    email="mock@example.com",
                    bio="Mock user profile for testing",
                    skills=["python", "testing", "mock"],
                    portfolio_url="https://github.com/mockuser",
                    location="Mock City",
                    experience_level="mid",
                    verification_status="Verified",
                    reputation_score=4.0,
                    created_at=1640995200,
                    updated_at=1640995200
                )
                logger.info(f"✅ Mock user profile returned: {mock_profile.name}")
                return mock_profile
            
            if not ICP_AGENT_AVAILABLE or not self.agent:
                logger.warning("⚠️ ic_agent not available, returning mock profile")
                return await self.get_user_profile(user_principal)
            
            # Call the identity contract
            result = await self.agent.query(
                canister_id=self.identity_canister_id,
                method="getUserProfile",
                arg={"userPrincipal": user_principal}
            )
            
            if result and result.get("Ok"):
                profile_data = result["Ok"]
                profile = UserProfile(
                    principal=profile_data.get("principal", ""),
                    name=profile_data.get("name", ""),
                    email=profile_data.get("email", ""),
                    bio=profile_data.get("bio", ""),
                    skills=profile_data.get("skills", []),
                    portfolio_url=profile_data.get("portfolio_url", ""),
                    location=profile_data.get("location", ""),
                    experience_level=profile_data.get("experience_level", ""),
                    verification_status=profile_data.get("verification_status", ""),
                    reputation_score=profile_data.get("reputation_score", 0.0),
                    created_at=profile_data.get("created_at", 0),
                    updated_at=profile_data.get("updated_at", 0)
                )
                logger.info(f"✅ User profile retrieved: {profile.name} ({profile.experience_level})")
                return profile
            else:
                logger.warning(f"⚠️ No profile found for principal: {user_principal}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error fetching user profile: {e}")
            return None
    
    async def store_chat(self, user_principal: str, message: str) -> Optional[int]:
        """Store chat message in ICP chat contract"""
        try:
            logger.info(f"💬 Storing chat message for user: {user_principal}")
            
            if self.mock_mode:
                # Return mock chat ID
                mock_chat_id = 12345
                logger.info(f"✅ Mock chat stored with ID: {mock_chat_id}")
                return mock_chat_id
            
            if not ICP_AGENT_AVAILABLE or not self.agent:
                logger.warning("⚠️ ic_agent not available, returning mock chat ID")
                return 12345
            
            # Call the chat contract
            result = await self.agent.update(
                canister_id=self.chat_canister_id,
                method="addChat",
                arg={"pesan": message}
            )
            
            if result and isinstance(result, int):
                logger.info(f"✅ Chat stored with ID: {result}")
                return result
            else:
                logger.warning(f"⚠️ Failed to store chat: {result}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error storing chat: {e}")
            return None
    
    async def get_user_chat_history(self, user_principal: str) -> List[ChatRecord]:
        """Get user's chat history from ICP chat contract"""
        try:
            logger.info(f"📚 Fetching chat history for user: {user_principal}")
            
            if self.mock_mode:
                # Return mock chat history
                mock_history = [
                    ChatRecord(
                        id=1,
                        user=user_principal,
                        message="Hello, I need help finding jobs",
                        timestamp=1640995200
                    ),
                    ChatRecord(
                        id=2,
                        user=user_principal,
                        message="Show me Python developer positions",
                        timestamp=1640995300
                    )
                ]
                logger.info(f"✅ Mock chat history returned: {len(mock_history)} records")
                return mock_history
            
            if not ICP_AGENT_AVAILABLE or not self.agent:
                logger.warning("⚠️ ic_agent not available, returning mock chat history")
                return await self.get_user_chat_history(user_principal)
            
            # Call the chat contract
            result = await self.agent.query(
                canister_id=self.chat_canister_id,
                method="getUserChats",
                arg={"user": user_principal}
            )
            
            if result:
                chat_records = []
                for chat_data in result:
                    chat_record = ChatRecord(
                        id=chat_data.get("id", 0),
                        user=chat_data.get("user", ""),
                        message=chat_data.get("pesan", ""),
                        timestamp=chat_data.get("timestamp", 0)
                    )
                    chat_records.append(chat_record)
                
                logger.info(f"✅ Retrieved {len(chat_records)} chat records")
                return chat_records
            else:
                logger.warning(f"⚠️ No chat history found for user: {user_principal}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error fetching chat history: {e}")
            return []

class PersonalizedChatbot:
    """Enhanced chatbot with ICP integration and personalization"""
    
    def __init__(self, icp_integration: ICPIntegration):
        self.icp_integration = icp_integration
        self.user_contexts: Dict[str, Dict[str, Any]] = {}
        
    def create_personalized_prompt(self, user_profile: UserProfile, user_message: str) -> str:
        """Create a personalized prompt based on user profile"""
        
        # Build context-aware prompt
        context_parts = [
            f"User Profile:",
            f"- Name: {user_profile.name}",
            f"- Experience Level: {user_profile.experience_level}",
            f"- Location: {user_profile.location}",
            f"- Skills: {', '.join(user_profile.skills)}",
            f"- Reputation Score: {user_profile.reputation_score}/5.0",
            f"- Bio: {user_profile.bio[:200]}...",
            "",
            f"User Request: {user_message}",
            "",
            "Based on this user's profile, provide a personalized response that considers:",
            "1. Their skill level and experience",
            "2. Their location preferences",
            "3. Their reputation and verification status",
            "4. Previous job preferences and patterns"
        ]
        
        return "\n".join(context_parts)
    
    def enhance_filters_with_profile(self, filters: Dict[str, Any], user_profile: UserProfile) -> Dict[str, Any]:
        """Enhance job filters based on user profile"""
        
        enhanced_filters = filters.copy()
        
        # Add user skills if not specified
        if not enhanced_filters.get("skills") and user_profile.skills:
            enhanced_filters["skills"] = user_profile.skills[:3]  # Top 3 skills
        
        # Add location preference if not specified
        if not enhanced_filters.get("location") and user_profile.location:
            enhanced_filters["location"] = user_profile.location
        
        # Adjust budget based on experience level
        if not enhanced_filters.get("budget_min"):
            if user_profile.experience_level.lower() == "senior":
                enhanced_filters["budget_min"] = 8000
                enhanced_filters["budget_max"] = 15000
            elif user_profile.experience_level.lower() == "mid":
                enhanced_filters["budget_min"] = 4000
                enhanced_filters["budget_max"] = 8000
            else:  # junior/entry
                enhanced_filters["budget_min"] = 2000
                enhanced_filters["budget_max"] = 4000
        
        # Add remote preference if user has good reputation
        if user_profile.reputation_score >= 4.0 and not enhanced_filters.get("remote"):
            enhanced_filters["remote"] = True
        
        logger.info(f"🎯 Enhanced filters with profile: {enhanced_filters}")
        return enhanced_filters
    
    async def get_personalized_response(self, user_principal: str, user_message: str) -> Dict[str, Any]:
        """Get personalized response based on user identity and context"""
        
        try:
            # Get user profile from ICP
            user_profile = await self.icp_integration.get_user_profile(user_principal)
            
            if user_profile:
                # Store chat in ICP
                await self.icp_integration.store_chat(user_principal, user_message)
                
                # Get chat history for context
                chat_history = await self.icp_integration.get_user_chat_history(user_principal)
                
                # Create personalized prompt
                personalized_prompt = self.create_personalized_prompt(user_profile, user_message)
                
                # Store user context
                self.user_contexts[user_principal] = {
                    "profile": user_profile,
                    "chat_history": chat_history,
                    "last_interaction": chat_history[-1].timestamp if chat_history else 0
                }
                
                return {
                    "personalized": True,
                    "user_profile": user_profile,
                    "enhanced_prompt": personalized_prompt,
                    "chat_history_count": len(chat_history),
                    "reputation_score": user_profile.reputation_score
                }
            else:
                # Fallback for users without profile
                logger.info(f"👤 No profile found for {user_principal}, using default response")
                return {
                    "personalized": False,
                    "message": "Welcome! I can help you find jobs. Consider creating a profile for personalized recommendations."
                }
                
        except Exception as e:
            logger.error(f"❌ Error in personalized response: {e}")
            return {
                "personalized": False,
                "error": str(e),
                "message": "I'm having trouble accessing your profile. Let me help you with a general job search."
            }
