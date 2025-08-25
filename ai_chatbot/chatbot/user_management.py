"""
User Management Module for ICP Identity Canister
Handles user profile creation, updates, and management
"""

import asyncio
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class UserProfileInput:
    """Input data for creating/updating user profile"""
    name: str
    email: str
    bio: str
    skills: List[str]
    portfolio_url: str
    location: str
    experience_level: str

@dataclass
class VerificationInput:
    """Input data for verification requests"""
    verification_type: str  # "email", "identity", "skills", "portfolio"
    verification_data: str

class UserManager:
    """Manages user operations with ICP identity canister"""
    
    def __init__(self, icp_integration):
        self.icp_integration = icp_integration
    
    async def create_user_profile(self, user_principal: str, profile_data: UserProfileInput) -> Dict[str, Any]:
        """Create a new user profile in the ICP canister"""
        try:
            logger.info(f"👤 Creating user profile for principal: {user_principal}")
            
            # Prepare profile data for the canister
            profile_args = {
                "name": profile_data.name,
                "email": profile_data.email,
                "bio": profile_data.bio,
                "skills": profile_data.skills,
                "portfolioUrl": profile_data.portfolio_url,
                "location": profile_data.location,
                "experienceLevel": profile_data.experience_level
            }
            
            logger.info(f"📝 Profile data: {json.dumps(profile_args, indent=2)}")
            
            # Call the identity contract to create/update profile
            result = await self.icp_integration.agent.update(
                canister_id=self.icp_integration.identity_canister_id,
                method="updateProfile",
                arg=profile_args
            )
            
            if result and result.get("Ok"):
                logger.info(f"✅ User profile created successfully for {user_principal}")
                return {
                    "success": True,
                    "message": "Profile created successfully",
                    "profile_id": user_principal
                }
            else:
                error_msg = result.get("Err", "Unknown error") if result else "No response"
                logger.error(f"❌ Failed to create profile: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "message": "Failed to create user profile"
                }
                
        except Exception as e:
            logger.error(f"❌ Error creating user profile: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Exception occurred while creating profile"
            }
    
    async def update_user_profile(self, user_principal: str, profile_data: UserProfileInput) -> Dict[str, Any]:
        """Update an existing user profile"""
        try:
            logger.info(f"🔄 Updating user profile for principal: {user_principal}")
            
            # Check if profile exists first
            existing_profile = await self.icp_integration.get_user_profile(user_principal)
            if not existing_profile:
                logger.warning(f"⚠️ Profile not found for {user_principal}, creating new one")
                return await self.create_user_profile(user_principal, profile_data)
            
            # Update existing profile
            profile_args = {
                "name": profile_data.name,
                "email": profile_data.email,
                "bio": profile_data.bio,
                "skills": profile_data.skills,
                "portfolioUrl": profile_data.portfolio_url,
                "location": profile_data.location,
                "experienceLevel": profile_data.experience_level
            }
            
            result = await self.icp_integration.agent.update(
                canister_id=self.icp_integration.identity_canister_id,
                method="updateProfile",
                arg=profile_args
            )
            
            if result and result.get("Ok"):
                logger.info(f"✅ User profile updated successfully for {user_principal}")
                return {
                    "success": True,
                    "message": "Profile updated successfully",
                    "profile_id": user_principal
                }
            else:
                error_msg = result.get("Err", "Unknown error") if result else "No response"
                logger.error(f"❌ Failed to update profile: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "message": "Failed to update user profile"
                }
                
        except Exception as e:
            logger.error(f"❌ Error updating user profile: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Exception occurred while updating profile"
            }
    
    async def submit_verification(self, user_principal: str, verification_data: VerificationInput) -> Dict[str, Any]:
        """Submit verification request for user"""
        try:
            logger.info(f"🔍 Submitting verification for user: {user_principal}")
            logger.info(f"📋 Verification type: {verification_data.verification_type}")
            
            verification_args = {
                "verificationType": verification_data.verification_type,
                "verificationData": verification_data.verification_data
            }
            
            result = await self.icp_integration.agent.update(
                canister_id=self.icp_integration.identity_canister_id,
                method="submitVerification",
                arg=verification_args
            )
            
            if result and result.get("Ok"):
                verification_id = result["Ok"]
                logger.info(f"✅ Verification submitted successfully: {verification_id}")
                return {
                    "success": True,
                    "verification_id": verification_id,
                    "message": "Verification request submitted successfully"
                }
            else:
                error_msg = result.get("Err", "Unknown error") if result else "No response"
                logger.error(f"❌ Failed to submit verification: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "message": "Failed to submit verification request"
                }
                
        except Exception as e:
            logger.error(f"❌ Error submitting verification: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Exception occurred while submitting verification"
            }
    
    async def get_user_verifications(self, user_principal: str) -> Dict[str, Any]:
        """Get all verifications for a user"""
        try:
            logger.info(f"📋 Fetching verifications for user: {user_principal}")
            
            verifications = await self.icp_integration.get_user_verifications(user_principal)
            
            return {
                "success": True,
                "verifications": [asdict(v) for v in verifications],
                "count": len(verifications)
            }
            
        except Exception as e:
            logger.error(f"❌ Error fetching verifications: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Exception occurred while fetching verifications"
            }
    
    async def add_reputation(self, target_user: str, job_id: str, rating: float, review: str) -> Dict[str, Any]:
        """Add reputation/review for a user"""
        try:
            logger.info(f"⭐ Adding reputation for user: {target_user}")
            logger.info(f"📊 Rating: {rating}/5.0, Job: {job_id}")
            
            reputation_args = {
                "userPrincipal": target_user,
                "jobId": job_id,
                "rating": rating,
                "review": review
            }
            
            result = await self.icp_integration.agent.update(
                canister_id=self.icp_integration.identity_canister_id,
                method="addReputation",
                arg=reputation_args
            )
            
            if result and result.get("Ok"):
                reputation_id = result["Ok"]
                logger.info(f"✅ Reputation added successfully: {reputation_id}")
                return {
                    "success": True,
                    "reputation_id": reputation_id,
                    "message": "Reputation added successfully"
                }
            else:
                error_msg = result.get("Err", "Unknown error") if result else "No response"
                logger.error(f"❌ Failed to add reputation: {error_msg}")
                return {
                    "success": False,
                    "error": error_msg,
                    "message": "Failed to add reputation"
                }
                
        except Exception as e:
            logger.error(f"❌ Error adding reputation: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Exception occurred while adding reputation"
            }

class MockUserManager:
    """Mock user manager for testing without real ICP connection"""
    
    def __init__(self):
        self.mock_profiles = {}
        self.mock_verifications = {}
        self.mock_reputations = {}
        logger.info("🤖 Mock user manager initialized for testing")
    
    async def create_user_profile(self, user_principal: str, profile_data: UserProfileInput) -> Dict[str, Any]:
        """Mock profile creation"""
        logger.info(f"🤖 Mock: Creating profile for {user_principal}")
        
        # Store mock profile
        self.mock_profiles[user_principal] = {
            "principal": user_principal,
            "name": profile_data.name,
            "email": profile_data.email,
            "bio": profile_data.bio,
            "skills": profile_data.skills,
            "portfolio_url": profile_data.portfolio_url,
            "location": profile_data.location,
            "experience_level": profile_data.experience_level,
            "verification_status": "Pending",
            "reputation_score": 0.0,
            "created_at": int(datetime.now().timestamp()),
            "updated_at": int(datetime.now().timestamp())
        }
        
        logger.info(f"✅ Mock: Profile created for {user_principal}")
        return {
            "success": True,
            "message": "Mock profile created successfully",
            "profile_id": user_principal
        }
    
    async def update_user_profile(self, user_principal: str, profile_data: UserProfileInput) -> Dict[str, Any]:
        """Mock profile update"""
        logger.info(f"🤖 Mock: Updating profile for {user_principal}")
        
        if user_principal in self.mock_profiles:
            self.mock_profiles[user_principal].update({
                "name": profile_data.name,
                "email": profile_data.email,
                "bio": profile_data.bio,
                "skills": profile_data.skills,
                "portfolio_url": profile_data.portfolio_url,
                "location": profile_data.location,
                "experience_level": profile_data.experience_level,
                "updated_at": int(datetime.now().timestamp())
            })
            
            return {
                "success": True,
                "message": "Mock profile updated successfully",
                "profile_id": user_principal
            }
        else:
            return await self.create_user_profile(user_principal, profile_data)
    
    async def submit_verification(self, user_principal: str, verification_data: VerificationInput) -> Dict[str, Any]:
        """Mock verification submission"""
        logger.info(f"🤖 Mock: Submitting verification for {user_principal}")
        
        verification_id = f"ver_{len(self.mock_verifications) + 1}"
        self.mock_verifications[verification_id] = {
            "id": verification_id,
            "user_principal": user_principal,
            "verification_type": verification_data.verification_type,
            "verification_data": verification_data.verification_data,
            "status": "Pending",
            "verified_at": None,
            "expires_at": None,
            "verifier": None
        }
        
        return {
            "success": True,
            "verification_id": verification_id,
            "message": "Mock verification submitted successfully"
        }
    
    def get_mock_profile(self, user_principal: str):
        """Get mock profile for testing"""
        return self.mock_profiles.get(user_principal)
    
    def get_mock_verifications(self, user_principal: str):
        """Get mock verifications for testing"""
        return [v for v in self.mock_verifications.values() if v["user_principal"] == user_principal]
