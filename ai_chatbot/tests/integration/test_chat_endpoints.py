#!/usr/bin/env python3
"""
Integration Tests for Chat Endpoints
Testing API endpoints with running server
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import requests
import json
import time
from datetime import datetime

class TestChatEndpoints:
    """Integration tests for chat endpoints"""
    
    def __init__(self):
        self.base_url = "http://localhost:8081"
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
    
    def test_health_endpoint(self):
        """Test server health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Health Endpoint", "PASS",
                    f"Server healthy - Status: {data.get('status')}"
                )
                return True
            else:
                self.log_test(
                    "Health Endpoint", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test(
                "Health Endpoint", "FAIL",
                "Cannot connect to server. Make sure it's running on port 8081"
            )
            return False
        except Exception as e:
            self.log_test(
                "Health Endpoint", "FAIL",
                f"Unexpected error: {str(e)}"
            )
            return False
    
    def test_basic_chat_endpoint(self):
        """Test basic chat endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "user_prompt": "Find me Java developer jobs remote work",
                    "user_principal": "test_user_123",
                    "top_k": 3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply_length = len(data.get('reply', ''))
                filters = data.get('filters', {})
                
                self.log_test(
                    "Basic Chat Endpoint", "PASS",
                    f"Reply length: {reply_length} chars, Filters: {len(filters)} items"
                )
                return True
            else:
                self.log_test(
                    "Basic Chat Endpoint", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Basic Chat Endpoint", "FAIL",
                f"Error: {str(e)}"
            )
            return False
    
    def test_personalized_chat_endpoint(self):
        """Test personalized chat endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/personalized",
                json={
                    "user_prompt": "Find me Python developer jobs",
                    "user_principal": "test_user_123",
                    "top_k": 3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                personalized = data.get('personalized', False)
                user_profile = data.get('user_profile', {})
                
                if personalized and user_profile:
                    self.log_test(
                        "Personalized Chat Endpoint", "PASS",
                        f"Personalized: {personalized}, User: {user_profile.get('name', 'Unknown')}"
                    )
                else:
                    self.log_test(
                        "Personalized Chat Endpoint", "WARNING",
                        f"Personalized: {personalized}, Profile: {bool(user_profile)}"
                    )
                return True
            else:
                self.log_test(
                    "Personalized Chat Endpoint", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Personalized Chat Endpoint", "FAIL",
                f"Error: {str(e)}"
            )
            return False
    
    def test_user_profile_endpoint(self):
        """Test user profile creation endpoint"""
        try:
            user_data = {
                "name": "Integration Test User",
                "email": "integration@test.com",
                "bio": "User for integration testing",
                "skills": ["python", "testing", "api"],
                "portfolio_url": "https://github.com/integrationtest",
                "location": "Test City",
                "experience_level": "mid"
            }
            
            response = requests.post(
                f"{self.base_url}/user/profile?user_principal=integration_test_123",
                json=user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "User Profile Endpoint", "PASS",
                    f"Profile created - ID: {data.get('profile_id')}"
                )
                return True
            else:
                self.log_test(
                    "User Profile Endpoint", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "User Profile Endpoint", "FAIL",
                f"Error: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🧪 INTEGRATION TESTS FOR CHAT ENDPOINTS")
        print("=" * 50)
        print(f"📍 Target Server: {self.base_url}")
        print(f"⏰ Start Time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        # Check server health first
        if not self.test_health_endpoint():
            print("\n❌ Server not accessible. Please start the server first:")
            print("   python main.py")
            return
        
        # Run integration tests
        tests = [
            ("Basic Chat", self.test_basic_chat_endpoint),
            ("Personalized Chat", self.test_personalized_chat_endpoint),
            ("User Profile", self.test_user_profile_endpoint)
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
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
        print("📊 INTEGRATION TEST RESULTS")
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

def main():
    """Main function to run integration tests"""
    print("🧪 CHAT ENDPOINTS INTEGRATION TESTS")
    print("=" * 50)
    print("This will test the actual running server endpoints")
    print("Make sure the server is running: python main.py")
    print("=" * 50)
    
    # Run integration tests
    test_suite = TestChatEndpoints()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()
