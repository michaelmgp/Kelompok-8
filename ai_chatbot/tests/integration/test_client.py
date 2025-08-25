#!/usr/bin/env python3
"""
Integration Tests for Chatbot Client
Testing client interactions and API calls
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import requests
import json
import time
from datetime import datetime

class TestChatbotClient:
    """Test chatbot client functionality"""
    
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.test_results = []
        self.session = requests.Session()
    
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
    
    def test_client_connection(self):
        """Test basic client connection"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                self.log_test(
                    "Client Connection", "PASS",
                    f"Successfully connected to {self.base_url}"
                )
                return True
            else:
                self.log_test(
                    "Client Connection", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except requests.exceptions.ConnectionError:
            self.log_test(
                "Client Connection", "FAIL",
                f"Cannot connect to {self.base_url}"
            )
            return False
        except Exception as e:
            self.log_test(
                "Client Connection", "FAIL",
                f"Unexpected error: {str(e)}"
            )
            return False
    
    def test_client_session_persistence(self):
        """Test that client session persists across requests"""
        try:
            # Make multiple requests to test session persistence
            responses = []
            for i in range(3):
                response = self.session.get(f"{self.base_url}/health", timeout=5)
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay between requests
            
            # All requests should succeed
            if all(status == 200 for status in responses):
                self.log_test(
                    "Session Persistence", "PASS",
                    f"Session maintained across {len(responses)} requests"
                )
                return True
            else:
                self.log_test(
                    "Session Persistence", "FAIL",
                    f"Session failed: {responses}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Session Persistence", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    def test_client_request_headers(self):
        """Test client request headers"""
        try:
            # Test with custom headers
            headers = {
                "User-Agent": "ChatbotTestClient/1.0",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            response = self.session.get(
                f"{self.base_url}/health",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.log_test(
                    "Request Headers", "PASS",
                    "Custom headers accepted successfully"
                )
                return True
            else:
                self.log_test(
                    "Request Headers", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Request Headers", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    def test_client_timeout_handling(self):
        """Test client timeout handling"""
        try:
            # Test with very short timeout
            start_time = time.time()
            
            try:
                response = self.session.get(
                    f"{self.base_url}/health",
                    timeout=0.001  # 1ms timeout - should fail
                )
                # If we get here, the request didn't timeout as expected
                self.log_test(
                    "Timeout Handling", "WARNING",
                    "Request completed despite very short timeout"
                )
                return True
                
            except requests.exceptions.Timeout:
                # Expected timeout
                duration = time.time() - start_time
                self.log_test(
                    "Timeout Handling", "PASS",
                    f"Timeout handled correctly after {duration:.3f}s"
                )
                return True
                
        except Exception as e:
            self.log_test(
                "Timeout Handling", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    def test_client_error_handling(self):
        """Test client error handling"""
        try:
            # Test with invalid endpoint
            response = self.session.get(f"{self.base_url}/invalid_endpoint", timeout=10)
            
            # Should get 404 or similar error
            if response.status_code >= 400:
                self.log_test(
                    "Error Handling", "PASS",
                    f"Properly handled invalid endpoint: {response.status_code}"
                )
                return True
            else:
                self.log_test(
                    "Error Handling", "WARNING",
                    f"Unexpected response for invalid endpoint: {response.status_code}"
                )
                return True
                
        except Exception as e:
            self.log_test(
                "Error Handling", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    def test_client_json_handling(self):
        """Test client JSON request/response handling"""
        try:
            # Test POST request with JSON
            test_data = {
                "user_prompt": "Test client JSON handling",
                "user_principal": "test_client_user",
                "top_k": 3
            }
            
            response = self.session.post(
                f"{self.base_url}/chat",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                # Try to parse JSON response
                try:
                    json_data = response.json()
                    self.log_test(
                        "JSON Handling", "PASS",
                        f"Successfully sent and received JSON data"
                    )
                    return True
                except json.JSONDecodeError:
                    self.log_test(
                        "JSON Handling", "FAIL",
                        "Response is not valid JSON"
                    )
                    return False
            else:
                self.log_test(
                    "JSON Handling", "FAIL",
                    f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "JSON Handling", "FAIL",
                f"Exception: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all client tests"""
        print("🧪 CHATBOT CLIENT INTEGRATION TESTS")
        print("=" * 50)
        print(f"📍 Target Server: {self.base_url}")
        print(f"⏰ Start Time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        # Check connection first
        if not self.test_client_connection():
            print("\n❌ Cannot connect to server. Please start the server first:")
            print("   python main.py")
            return
        
        # Run client tests
        tests = [
            ("Session Persistence", self.test_client_session_persistence),
            ("Request Headers", self.test_client_request_headers),
            ("Timeout Handling", self.test_client_timeout_handling),
            ("Error Handling", self.test_client_error_handling),
            ("JSON Handling", self.test_client_json_handling)
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
        print("📊 CLIENT TEST RESULTS")
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
    """Main function to run client tests"""
    print("🧪 CHATBOT CLIENT INTEGRATION TESTS")
    print("=" * 50)
    print("Testing client functionality and API interactions")
    print("Make sure the server is running: python main.py")
    print("=" * 50)
    
    # Run client tests
    test_suite = TestChatbotClient()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()
