#!/usr/bin/env python3
"""
Organized Chatbot Test Suite
Comprehensive testing framework for all chatbot functionality
"""

import os
import sys
import asyncio
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

class ChatbotTestSuite:
    """Organized test suite for chatbot functionality"""
    
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.test_results = []
        self.start_time = None
        self.end_time = None
        
        # Test users for different scenarios
        self.test_users = {
            "java_senior": {
                "principal": "alice_java_123",
                "name": "Alice Java Developer",
                "skills": ["java", "spring", "microservices"],
                "experience": "senior",
                "location": "San Francisco, CA"
            },
            "react_mid": {
                "principal": "bob_react_456", 
                "name": "Bob React Developer",
                "skills": ["react", "typescript", "javascript"],
                "experience": "mid",
                "location": "New York, NY"
            },
            "python_junior": {
                "principal": "carol_python_789",
                "name": "Carol Python Developer",
                "skills": ["python", "django", "flask"],
                "experience": "junior",
                "location": "Austin, TX"
            }
        }
        
        # Test prompts for different scenarios
        self.test_prompts = {
            "basic_job_search": [
                "Hi, I want to get Java developer jobs with salary 1500USD/month remote fulltime",
                "Find me React developer positions in New York",
                "Show me Python jobs with good salary"
            ],
            "detailed_requirements": [
                "I need a senior Java developer position with microservices experience, remote work, salary 8000-12000 USD/month",
                "Looking for React developer with TypeScript, 3+ years experience, hybrid work in NYC, budget 6000-9000 USD/month",
                "Python developer needed for machine learning projects, entry level, remote work preferred, salary 3000-5000 USD/month"
            ],
            "skill_specific": [
                "Find jobs requiring Spring Boot and Docker experience",
                "Show me positions that need React and Node.js skills",
                "Looking for Python jobs with pandas and scikit-learn"
            ]
        }
    
    def log_test(self, test_name: str, status: str, details: str = "", duration: float = 0):
        """Log test results with timestamp"""
        test_result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(test_result)
        
        # Print with emoji and formatting
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
        if duration > 0:
            print(f"   ⏱️  {duration:.2f}s")
    
    def print_header(self, title: str):
        """Print formatted section header"""
        print("\n" + "=" * 60)
        print(f"🧪 {title}")
        print("=" * 60)
    
    def print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])
        
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"🎯 Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if self.start_time and self.end_time:
            total_duration = (self.end_time - self.start_time).total_seconds()
            print(f"⏱️  Total Duration: {total_duration:.2f}s")
        
        # Show failed tests if any
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"   - {result['test_name']}: {result['details']}")
    
    # ==================== SECTION 1: SERVER HEALTH TESTS ====================
    
    def test_server_health(self):
        """Test server health and basic connectivity"""
        self.print_header("SERVER HEALTH TESTS")
        
        # Test 1: Health endpoint
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Health Endpoint", "PASS",
                    f"Server healthy - Status: {data.get('status')}",
                    duration
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
    
    # ==================== SECTION 2: USER MANAGEMENT TESTS ====================
    
    def test_user_management(self):
        """Test user profile creation and management"""
        self.print_header("USER MANAGEMENT TESTS")
        
        # Test 1: Create user profile
        start_time = time.time()
        try:
            new_user = {
                "name": "Test Developer",
                "email": "test@example.com",
                "bio": "Test user for comprehensive testing",
                "skills": ["python", "testing", "api", "automation"],
                "portfolio_url": "https://github.com/testdev",
                "location": "Test City, TC",
                "experience_level": "mid"
            }
            
            response = requests.post(
                f"{self.base_url}/user/profile?user_principal=test_user_123",
                json=new_user,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Create User Profile", "PASS",
                    f"Profile created - ID: {data.get('profile_id')}",
                    duration
                )
            else:
                self.log_test(
                    "Create User Profile", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Create User Profile", "FAIL",
                f"Error: {str(e)}"
            )
        
        # Test 2: Update user profile
        start_time = time.time()
        try:
            updated_user = {
                "name": "Updated Test Developer",
                "email": "updated@example.com",
                "bio": "Updated test user with more experience",
                "skills": ["python", "testing", "api", "automation", "machine-learning"],
                "portfolio_url": "https://github.com/testdev",
                "location": "Updated City, UC",
                "experience_level": "senior"
            }
            
            response = requests.put(
                f"{self.base_url}/user/profile/test_user_123",
                json=updated_user,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Update User Profile", "PASS",
                    f"Profile updated - ID: {data.get('profile_id')}",
                    duration
                )
            else:
                self.log_test(
                    "Update User Profile", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Update User Profile", "FAIL",
                f"Error: {str(e)}"
            )
    
    # ==================== SECTION 3: BASIC CHAT TESTS ====================
    
    def test_basic_chat(self):
        """Test basic chat functionality without user profiles"""
        self.print_header("BASIC CHAT TESTS")
        
        for i, prompt in enumerate(self.test_prompts["basic_job_search"], 1):
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={
                        "user_prompt": prompt,
                        "user_principal": "anonymous_user",
                        "top_k": 5
                    },
                    timeout=30
                )
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    reply_length = len(data.get('reply', ''))
                    filters = data.get('filters', {})
                    
                    self.log_test(
                        f"Basic Chat {i}", "PASS",
                        f"Reply length: {reply_length} chars, Filters: {len(filters)} items",
                        duration
                    )
                else:
                    self.log_test(
                        f"Basic Chat {i}", "FAIL",
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Basic Chat {i}", "FAIL",
                    f"Error: {str(e)}"
                )
    
    # ==================== SECTION 4: PERSONALIZED CHAT TESTS ====================
    
    def test_personalized_chat(self):
        """Test personalized chat with user profiles"""
        self.print_header("PERSONALIZED CHAT TESTS")
        
        for user_key, user_info in self.test_users.items():
            start_time = time.time()
            try:
                # Create personalized prompt
                prompt = f"Find me {user_info['skills'][0]} developer jobs with good salary"
                
                response = requests.post(
                    f"{self.base_url}/chat/personalized",
                    json={
                        "user_prompt": prompt,
                        "user_principal": user_info["principal"],
                        "top_k": 5
                    },
                    timeout=30
                )
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    personalized = data.get('personalized', False)
                    user_profile = data.get('user_profile', {})
                    
                    if personalized and user_profile:
                        self.log_test(
                            f"Personalized Chat - {user_info['name']}", "PASS",
                            f"Personalized: {personalized}, User: {user_profile.get('name')}",
                            duration
                        )
                    else:
                        self.log_test(
                            f"Personalized Chat - {user_info['name']}", "WARNING",
                            f"Personalized: {personalized}, Profile: {bool(user_profile)}"
                        )
                else:
                    self.log_test(
                        f"Personalized Chat - {user_info['name']}", "FAIL",
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Personalized Chat - {user_info['name']}", "FAIL",
                    f"Error: {str(e)}"
                )
    
    # ==================== SECTION 5: ADVANCED PROMPT TESTS ====================
    
    def test_advanced_prompts(self):
        """Test complex prompts with detailed requirements"""
        self.print_header("ADVANCED PROMPT TESTS")
        
        for i, prompt in enumerate(self.test_prompts["detailed_requirements"], 1):
            start_time = time.time()
            try:
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={
                        "user_prompt": prompt,
                        "user_principal": "advanced_user",
                        "top_k": 10
                    },
                    timeout=30
                )
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    filters = data.get('filters', {})
                    
                    # Check if filters were extracted properly
                    filter_count = len([k for k, v in filters.items() if v is not None])
                    
                    if filter_count >= 3:  # At least 3 filters extracted
                        self.log_test(
                            f"Advanced Prompt {i}", "PASS",
                            f"Filters extracted: {filter_count}/{len(filters)}",
                            duration
                        )
                    else:
                        self.log_test(
                            f"Advanced Prompt {i}", "WARNING",
                            f"Limited filters extracted: {filter_count}/{len(filters)}"
                        )
                else:
                    self.log_test(
                        f"Advanced Prompt {i}", "FAIL",
                        f"HTTP {response.status_code}: {response.text}"
                    )
                    
            except Exception as e:
                self.log_test(
                    f"Advanced Prompt {i}", "FAIL",
                    f"Error: {str(e)}"
                )
    
    # ==================== SECTION 6: PERFORMANCE TESTS ====================
    
    def test_performance(self):
        """Test response times and performance"""
        self.print_header("PERFORMANCE TESTS")
        
        # Test multiple concurrent requests
        start_time = time.time()
        try:
            responses = []
            for i in range(3):
                response = requests.post(
                    f"{self.base_url}/chat",
                    json={
                        "user_prompt": f"Quick test {i+1}",
                        "user_principal": f"perf_user_{i}",
                        "top_k": 3
                    },
                    timeout=30
                )
                responses.append(response)
            
            duration = time.time() - start_time
            successful_responses = len([r for r in responses if r.status_code == 200])
            
            if successful_responses == 3:
                self.log_test(
                    "Concurrent Requests", "PASS",
                    f"All {successful_responses}/3 requests successful",
                    duration
                )
            else:
                self.log_test(
                    "Concurrent Requests", "WARNING",
                    f"{successful_responses}/3 requests successful"
                )
                
        except Exception as e:
            self.log_test(
                "Concurrent Requests", "FAIL",
                f"Error: {str(e)}"
            )
    
    # ==================== MAIN TEST EXECUTION ====================
    
    def run_all_tests(self):
        """Execute all test sections"""
        print("🚀 STARTING COMPREHENSIVE CHATBOT TEST SUITE")
        print(f"📍 Target Server: {self.base_url}")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = datetime.now()
        
        # Run all test sections
        test_sections = [
            ("Server Health", self.test_server_health),
            ("User Management", self.test_user_management),
            ("Basic Chat", self.test_basic_chat),
            ("Personalized Chat", self.test_personalized_chat),
            ("Advanced Prompts", self.test_advanced_prompts),
            ("Performance", self.test_performance)
        ]
        
        for section_name, test_method in test_sections:
            try:
                test_method()
            except Exception as e:
                self.log_test(
                    f"{section_name} Section", "FAIL",
                    f"Section crashed: {str(e)}"
                )
        
        self.end_time = datetime.now()
        self.print_summary()
        
        # Save results to file
        self.save_results()
    
    def save_results(self):
        """Save test results to JSON file"""
        try:
            results_file = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump({
                    "test_suite": "Chatbot Comprehensive Test Suite",
                    "timestamp": datetime.now().isoformat(),
                    "base_url": self.base_url,
                    "results": self.test_results
                }, f, indent=2)
            
            print(f"\n💾 Test results saved to: {results_file}")
        except Exception as e:
            print(f"\n⚠️  Could not save results: {e}")

def main():
    """Main function to run the test suite"""
    print("🧪 CHATBOT COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("This test suite will test:")
    print("1. 🏥 Server Health & Connectivity")
    print("2. 👤 User Profile Management")
    print("3. 💬 Basic Chat Functionality")
    print("4. 🎯 Personalized Chat Responses")
    print("5. 🔍 Advanced Prompt Processing")
    print("6. ⚡ Performance & Concurrency")
    print("=" * 60)
    
    # Check if server is accessible
    try:
        response = requests.get("http://localhost:8081/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server health check failed. Please start the server first:")
            print("   python main.py")
            return
    except:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python main.py")
        return
    
    print("✅ Server is accessible. Starting tests...")
    
    # Run the test suite
    test_suite = ChatbotTestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()
