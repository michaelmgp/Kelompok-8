#!/usr/bin/env python3
"""
Integration Tests for ICP Integration
Testing ICP canister interactions and user management
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import asyncio
import json
from datetime import datetime
from chatbot.user_management import MockUserManager, UserProfileInput, VerificationInput

class TestICPIntegration:
    """Test ICP integration functionality"""
    
    def __init__(self):
        self.user_manager = MockUserManager()
        self.test_results = []
    
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        test_result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(test_result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
    
    async def test_create_user_profile(self):
        """Test user profile creation"""
        try:
            user_input = UserProfileInput(
                name="Test User",
                email="test@example.com",
                bio="Test user for ICP integration",
                skills=["python", "icp", "blockchain"],
                portfolio_url="https://github.com/testuser",
                location="Test City",
                experience_level="mid"
            )
            
            result = await self.user_manager.create_user_profile(
                user_principal="test_principal_123",
                user_input=user_input
            )
            
            if result and result.get("profile_id"):
                self.log_test(
                    "Create User Profile", "PASS",
                    f"Profile created with ID: {result['profile_id']}"
                )
                return True
            else:
                self.log_test(
                    "Create User Profile", "FAIL",
                    "No profile ID returned"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Create User Profile", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    async def test_update_user_profile(self):
        """Test user profile update"""
        try:
            # First create a profile
            user_input = UserProfileInput(
                name="Original User",
                email="original@example.com",
                bio="Original bio",
                skills=["python"],
                portfolio_url="https://github.com/original",
                location="Original City",
                experience_level="junior"
            )
            
            await self.user_manager.create_user_profile(
                user_principal="update_test_123",
                user_input=user_input
            )
            
            # Now update it
            updated_input = UserProfileInput(
                name="Updated User",
                email="updated@example.com",
                bio="Updated bio with more experience",
                skills=["python", "icp", "advanced"],
                portfolio_url="https://github.com/updated",
                location="Updated City",
                experience_level="senior"
            )
            
            result = await self.user_manager.update_user_profile(
                user_principal="update_test_123",
                user_input=updated_input
            )
            
            if result and result.get("profile_id"):
                self.log_test(
                    "Update User Profile", "PASS",
                    f"Profile updated with ID: {result['profile_id']}"
                )
                return True
            else:
                self.log_test(
                    "Update User Profile", "FAIL",
                    "No profile ID returned from update"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Update User Profile", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    async def test_submit_verification(self):
        """Test verification submission"""
        try:
            verification_input = VerificationInput(
                document_type="passport",
                document_url="https://example.com/passport.pdf",
                verification_notes="Passport verification for identity"
            )
            
            result = await self.user_manager.submit_verification(
                user_principal="verification_test_123",
                verification_input=verification_input
            )
            
            if result and result.get("verification_id"):
                self.log_test(
                    "Submit Verification", "PASS",
                    f"Verification submitted with ID: {result['verification_id']}"
                )
                return True
            else:
                self.log_test(
                    "Submit Verification", "FAIL",
                    "No verification ID returned"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Submit Verification", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    async def test_get_user_verifications(self):
        """Test getting user verifications"""
        try:
            # First submit a verification
            verification_input = VerificationInput(
                document_type="driver_license",
                document_url="https://example.com/license.pdf",
                verification_notes="Driver license verification"
            )
            
            await self.user_manager.submit_verification(
                user_principal="get_verifications_test_123",
                verification_input=verification_input
            )
            
            # Now get the verifications
            verifications = await self.user_manager.get_user_verifications(
                user_principal="get_verifications_test_123"
            )
            
            if verifications and len(verifications) > 0:
                self.log_test(
                    "Get User Verifications", "PASS",
                    f"Found {len(verifications)} verifications"
                )
                return True
            else:
                self.log_test(
                    "Get User Verifications", "FAIL",
                    "No verifications returned"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Get User Verifications", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    async def test_add_reputation(self):
        """Test reputation system"""
        try:
            result = await self.user_manager.add_reputation(
                user_principal="reputation_test_123",
                score=5,
                reason="Excellent work on ICP project"
            )
            
            if result and result.get("reputation_id"):
                self.log_test(
                    "Add Reputation", "PASS",
                    f"Reputation added with ID: {result['reputation_id']}"
                )
                return True
            else:
                self.log_test(
                    "Add Reputation", "FAIL",
                    "No reputation ID returned"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Add Reputation", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    async def run_all_tests(self):
        """Run all ICP integration tests"""
        print("🧪 ICP INTEGRATION TESTS")
        print("=" * 50)
        print(f"⏰ Start Time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        # Run all tests
        tests = [
            ("Create User Profile", self.test_create_user_profile),
            ("Update User Profile", self.test_update_user_profile),
            ("Submit Verification", self.test_submit_verification),
            ("Get User Verifications", self.test_get_user_verifications),
            ("Add Reputation", self.test_add_reputation)
        ]
        
        for test_name, test_func in tests:
            try:
                await test_func()
            except Exception as e:
                self.log_test(
                    f"{test_name} Test", "FAIL",
                    f"Test crashed: {str(e)}"
                )
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 50)
        print("📊 ICP INTEGRATION TEST RESULTS")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"🎯 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"   - {result['test_name']}: {result['details']}")

async def main():
    """Main function to run ICP integration tests"""
    print("🧪 ICP INTEGRATION TEST SUITE")
    print("=" * 50)
    print("Testing ICP canister integration functionality")
    print("=" * 50)
    
    # Run tests
    test_suite = TestICPIntegration()
    await test_suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
