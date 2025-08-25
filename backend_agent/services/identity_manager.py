import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import jwt
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class UserProfile:
    """User profile data structure"""
    user_id: str
    username: str
    email: str
    skills: List[str]
    experience_level: str
    preferred_platforms: List[str]
    location: Optional[str]
    hourly_rate: Optional[float]
    bio: Optional[str]
    portfolio_links: List[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    is_active: bool = True

@dataclass
class UserSession:
    """User session data"""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_valid: bool = True

class IdentityManager:
    """
    Manages user identities, profiles, and authentication
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.secret_key = config.get("jwt_secret", "default_secret_key")
        self.jwt_expiry_hours = config.get("jwt_expiry_hours", 24)
        self.max_sessions_per_user = config.get("max_sessions_per_user", 5)
        
        # In-memory storage (replace with database in production)
        self.users: Dict[str, UserProfile] = {}
        self.sessions: Dict[str, UserSession] = {}
        self.user_sessions: Dict[str, List[str]] = defaultdict(list)
        
        # Initialize with some sample users
        self._initialize_sample_users()
    
    def _initialize_sample_users(self):
        """Initialize with sample user data for testing"""
        sample_users = [
            {
                "user_id": "user_123",
                "username": "john_developer",
                "email": "john@example.com",
                "skills": ["python", "javascript", "react", "node.js"],
                "experience_level": "intermediate",
                "preferred_platforms": ["upwork", "fiverr"],
                "location": "New York, USA",
                "hourly_rate": 45.0,
                "bio": "Full-stack developer with 3 years of experience",
                "portfolio_links": ["https://github.com/john", "https://john.dev"],
                "created_at": datetime.utcnow() - timedelta(days=30),
                "updated_at": datetime.utcnow() - timedelta(days=5),
                "last_login": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "user_id": "user_456",
                "username": "sarah_designer",
                "email": "sarah@example.com",
                "skills": ["ui/ux", "graphic design", "figma", "photoshop"],
                "experience_level": "expert",
                "preferred_platforms": ["fiverr"],
                "location": "London, UK",
                "hourly_rate": 65.0,
                "bio": "Creative designer specializing in brand identity",
                "portfolio_links": ["https://behance.net/sarah", "https://sarah.design"],
                "created_at": datetime.utcnow() - timedelta(days=60),
                "updated_at": datetime.utcnow() - timedelta(days=1),
                "last_login": datetime.utcnow() - timedelta(hours=12)
            }
        ]
        
        for user_data in sample_users:
            user = UserProfile(**user_data)
            self.users[user.user_id] = user
    
    async def create_user(
        self, 
        username: str, 
        email: str, 
        password: str,
        **profile_data
    ) -> Optional[str]:
        """
        Create a new user account
        """
        try:
            # Check if username or email already exists
            if self._username_exists(username):
                logger.warning(f"Username already exists: {username}")
                return None
            
            if self._email_exists(email):
                logger.warning(f"Email already exists: {email}")
                return None
            
            # Generate user ID
            user_id = self._generate_user_id(username, email)
            
            # Hash password
            hashed_password = self._hash_password(password)
            
            # Create user profile
            user_profile = UserProfile(
                user_id=user_id,
                username=username,
                email=email,
                skills=profile_data.get("skills", []),
                experience_level=profile_data.get("experience_level", "beginner"),
                preferred_platforms=profile_data.get("preferred_platforms", ["upwork", "fiverr"]),
                location=profile_data.get("location"),
                hourly_rate=profile_data.get("hourly_rate"),
                bio=profile_data.get("bio"),
                portfolio_links=profile_data.get("portfolio_links", []),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                last_login=None
            )
            
            # Store user (in production, this would be in a database)
            self.users[user_id] = user_profile
            
            # Store hashed password separately (in production, use proper auth system)
            # For now, we'll store it in the user object (not secure for production)
            user_profile.hashed_password = hashed_password
            
            logger.info(f"Created new user: {username} ({user_id})")
            return user_id
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    async def authenticate_user(
        self, 
        username: str, 
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user and create session
        """
        try:
            # Find user by username or email
            user = self._find_user_by_username_or_email(username)
            if not user:
                logger.warning(f"Authentication failed: user not found - {username}")
                return None
            
            # Check password
            if not self._verify_password(password, getattr(user, 'hashed_password', '')):
                logger.warning(f"Authentication failed: invalid password for {username}")
                return None
            
            # Check if user is active
            if not user.is_active:
                logger.warning(f"Authentication failed: inactive user - {username}")
                return None
            
            # Create session
            session = await self._create_user_session(
                user.user_id, ip_address, user_agent
            )
            
            # Update last login
            user.last_login = datetime.utcnow()
            user.updated_at = datetime.utcnow()
            
            # Generate JWT token
            token = self._generate_jwt_token(user.user_id, session.session_id)
            
            logger.info(f"User authenticated successfully: {username}")
            
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "token": token,
                "session_id": session.session_id,
                "expires_at": session.expires_at.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    async def validate_token(self, token: str) -> Optional[str]:
        """
        Validate JWT token and return user ID
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            session_id = payload.get("session_id")
            
            if not user_id or not session_id:
                return None
            
            # Check if session is valid
            session = self.sessions.get(session_id)
            if not session or not session.is_valid:
                return None
            
            # Check if session has expired
            if datetime.utcnow() > session.expires_at:
                await self._invalidate_session(session_id)
                return None
            
            # Check if user exists and is active
            user = self.users.get(user_id)
            if not user or not user.is_active:
                return None
            
            return user_id
            
        except jwt.ExpiredSignatureError:
            logger.info("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error validating token: {e}")
            return None
    
    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by ID
        """
        return self.users.get(user_id)
    
    async def update_user_profile(
        self, 
        user_id: str, 
        profile_data: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """
        Update user profile
        """
        try:
            user = self.users.get(user_id)
            if not user:
                return None
            
            # Update allowed fields
            allowed_fields = {
                "skills", "experience_level", "preferred_platforms", 
                "location", "hourly_rate", "bio", "portfolio_links"
            }
            
            for field, value in profile_data.items():
                if field in allowed_fields and hasattr(user, field):
                    setattr(user, field, value)
            
            user.updated_at = datetime.utcnow()
            
            logger.info(f"Updated profile for user: {user_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            return None
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Delete user account
        """
        try:
            if user_id not in self.users:
                return False
            
            # Remove user
            del self.users[user_id]
            
            # Remove all user sessions
            if user_id in self.user_sessions:
                for session_id in self.user_sessions[user_id]:
                    if session_id in self.sessions:
                        del self.sessions[session_id]
                del self.user_sessions[user_id]
            
            logger.info(f"Deleted user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
    
    async def logout_user(self, session_id: str) -> bool:
        """
        Logout user by invalidating session
        """
        try:
            await self._invalidate_session(session_id)
            logger.info(f"User logged out: {session_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging out user: {e}")
            return False
    
    async def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all active sessions for a user
        """
        try:
            session_ids = self.user_sessions.get(user_id, [])
            sessions = []
            
            for session_id in session_ids:
                session = self.sessions.get(session_id)
                if session and session.is_valid:
                    sessions.append(asdict(session))
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting user sessions: {e}")
            return []
    
    async def get_user_count(self) -> int:
        """Get total number of users"""
        return len(self.users)
    
    def _username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return any(user.username == username for user in self.users.values())
    
    def _email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return any(user.email == email for user in self.users.values())
    
    def _generate_user_id(self, username: str, email: str) -> str:
        """Generate unique user ID"""
        timestamp = str(int(datetime.utcnow().timestamp()))
        unique_string = f"{username}_{email}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self._hash_password(password) == hashed_password
    
    def _find_user_by_username_or_email(self, identifier: str) -> Optional[UserProfile]:
        """Find user by username or email"""
        for user in self.users.values():
            if user.username == identifier or user.email == identifier:
                return user
        return None
    
    async def _create_user_session(
        self, 
        user_id: str, 
        ip_address: Optional[str], 
        user_agent: Optional[str]
    ) -> UserSession:
        """Create a new user session"""
        # Clean up old sessions if user has too many
        if user_id in self.user_sessions:
            user_session_ids = self.user_sessions[user_id]
            if len(user_session_ids) >= self.max_sessions_per_user:
                # Remove oldest session
                oldest_session_id = user_session_ids[0]
                await self._invalidate_session(oldest_session_id)
                user_session_ids.pop(0)
        
        # Create new session
        session_id = self._generate_session_id(user_id)
        expires_at = datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours)
        
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Store session
        self.sessions[session_id] = session
        
        # Add to user's session list
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        self.user_sessions[user_id].append(session_id)
        
        return session
    
    async def _invalidate_session(self, session_id: str):
        """Invalidate a user session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.is_valid = False
            
            # Remove from user's session list
            user_id = session.user_id
            if user_id in self.user_sessions:
                try:
                    self.user_sessions[user_id].remove(session_id)
                except ValueError:
                    pass
    
    def _generate_session_id(self, user_id: str) -> str:
        """Generate unique session ID"""
        timestamp = str(int(datetime.utcnow().timestamp()))
        unique_string = f"{user_id}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:16]
    
    def _generate_jwt_token(self, user_id: str, session_id: str) -> str:
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "session_id": session_id,
            "exp": datetime.utcnow() + timedelta(hours=self.jwt_expiry_hours),
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
    
    async def cleanup(self):
        """Cleanup expired sessions and invalid data"""
        try:
            now = datetime.utcnow()
            expired_sessions = []
            
            # Find expired sessions
            for session_id, session in self.sessions.items():
                if now > session.expires_at:
                    expired_sessions.append(session_id)
            
            # Remove expired sessions
            for session_id in expired_sessions:
                await self._invalidate_session(session_id)
                del self.sessions[session_id]
            
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get identity manager statistics"""
        active_sessions = sum(1 for s in self.sessions.values() if s.is_valid)
        total_sessions = len(self.sessions)
        
        return {
            "total_users": len(self.users),
            "active_users": sum(1 for u in self.users.values() if u.is_active),
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "expired_sessions": total_sessions - active_sessions
        } 