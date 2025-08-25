#!/usr/bin/env python3
"""
Performance Tests for Chatbot
Testing load handling and concurrent requests
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import requests
import time
import threading
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class PerformanceTester:
    """Performance testing for chatbot endpoints"""
    
    def __init__(self):
        self.base_url = "http://localhost:8081"
        self.test_results = []
        self.response_times = []
    
    def log_test(self, test_name: str, status: str, details: str = "", duration: float = 0):
        """Log test results"""
        test_result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(test_result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
        if duration > 0:
            print(f"   ⏱️  {duration:.2f}s")
    
    def single_request_test(self, prompt: str, user_id: str = "perf_user"):
        """Test single request performance"""
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={
                    "user_prompt": prompt,
                    "user_principal": user_id,
                    "top_k": 3
                },
                timeout=30
            )
            
            duration = time.time() - start_time
            self.response_times.append(duration)
            
            if response.status_code == 200:
                return True, duration, None
            else:
                return False, duration, f"HTTP {response.status_code}"
                
        except Exception as e:
            duration = time.time() - start_time
            return False, duration, str(e)
    
    def concurrent_requests_test(self, num_requests: int = 10):
        """Test concurrent request handling"""
        print(f"\n🚀 Testing {num_requests} concurrent requests...")
        
        prompts = [
            "Find me Java developer jobs",
            "Show Python developer positions",
            "Looking for React developer roles",
            "Need backend developer with Node.js",
            "Find frontend developer with Vue.js",
            "Show me DevOps engineer positions",
            "Looking for data scientist roles",
            "Need mobile developer with Flutter",
            "Find QA engineer positions",
            "Show me product manager roles"
        ]
        
        start_time = time.time()
        successful_requests = 0
        failed_requests = 0
        
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            # Submit all requests
            future_to_prompt = {
                executor.submit(self.single_request_test, prompt, f"user_{i}"): prompt
                for i, prompt in enumerate(prompts[:num_requests])
            }
            
            # Collect results
            for future in as_completed(future_to_prompt):
                prompt = future_to_prompt[future]
                try:
                    success, duration, error = future.result()
                    if success:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                        print(f"   ❌ Failed: {prompt[:30]}... - {error}")
                except Exception as e:
                    failed_requests += 1
                    print(f"   ❌ Exception: {prompt[:30]}... - {str(e)}")
        
        total_duration = time.time() - start_time
        
        # Calculate statistics
        if self.response_times:
            avg_response_time = statistics.mean(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
            median_response_time = statistics.median(self.response_times)
            
            self.log_test(
                "Concurrent Requests", "PASS" if failed_requests == 0 else "WARNING",
                f"Success: {successful_requests}/{num_requests}, "
                f"Avg: {avg_response_time:.2f}s, "
                f"Min: {min_response_time:.2f}s, "
                f"Max: {max_response_time:.2f}s, "
                f"Median: {median_response_time:.2f}s",
                total_duration
            )
        else:
            self.log_test(
                "Concurrent Requests", "FAIL",
                "No successful responses to measure"
            )
    
    def load_test(self, requests_per_second: int = 5, duration_seconds: int = 30):
        """Test sustained load over time"""
        print(f"\n📈 Load Test: {requests_per_second} req/s for {duration_seconds} seconds...")
        
        total_requests = requests_per_second * duration_seconds
        successful_requests = 0
        failed_requests = 0
        
        start_time = time.time()
        request_interval = 1.0 / requests_per_second
        
        for i in range(total_requests):
            request_start = time.time()
            
            success, duration, error = self.single_request_test(
                f"Load test request {i+1}",
                f"load_user_{i}"
            )
            
            if success:
                successful_requests += 1
            else:
                failed_requests += 1
            
            # Wait for next request interval
            elapsed = time.time() - request_start
            if elapsed < request_interval:
                time.sleep(request_interval - elapsed)
        
        total_duration = time.time() - start_time
        
        # Calculate actual RPS
        actual_rps = successful_requests / total_duration
        
        self.log_test(
            "Sustained Load Test", "PASS" if failed_requests == 0 else "WARNING",
            f"Target: {requests_per_second} req/s, Actual: {actual_rps:.1f} req/s, "
            f"Success: {successful_requests}/{total_requests}",
            total_duration
        )
    
    def response_time_analysis(self):
        """Analyze response time distribution"""
        if not self.response_times:
            print("⚠️  No response times to analyze")
            return
        
        print(f"\n📊 Response Time Analysis")
        print("=" * 40)
        
        # Basic statistics
        avg_time = statistics.mean(self.response_times)
        min_time = min(self.response_times)
        max_time = max(self.response_times)
        median_time = statistics.median(self.response_times)
        
        print(f"📈 Total Requests: {len(self.response_times)}")
        print(f"⏱️  Average Response Time: {avg_time:.2f}s")
        print(f"⚡ Fastest Response: {min_time:.2f}s")
        print(f"🐌 Slowest Response: {max_time:.2f}s")
        print(f"📊 Median Response Time: {median_time:.2f}s")
        
        # Percentiles
        sorted_times = sorted(self.response_times)
        p95 = sorted_times[int(0.95 * len(sorted_times))]
        p99 = sorted_times[int(0.99 * len(sorted_times))]
        
        print(f"📊 95th Percentile: {p95:.2f}s")
        print(f"📊 99th Percentile: {p99:.2f}s")
        
        # Performance categories
        fast_responses = len([t for t in self.response_times if t < 1.0])
        medium_responses = len([t for t in self.response_times if 1.0 <= t < 3.0])
        slow_responses = len([t for t in self.response_times if t >= 3.0])
        
        print(f"\n🚀 Fast (<1s): {fast_responses} ({fast_responses/len(self.response_times)*100:.1f}%)")
        print(f"⚡ Medium (1-3s): {medium_responses} ({medium_responses/len(self.response_times)*100:.1f}%)")
        print(f"🐌 Slow (>3s): {slow_responses} ({slow_responses/len(self.response_times)*100:.1f}%)")
    
    def run_performance_suite(self):
        """Run complete performance test suite"""
        print("🚀 PERFORMANCE TEST SUITE")
        print("=" * 50)
        print(f"📍 Target Server: {self.base_url}")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Check server health first
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code != 200:
                print("❌ Server health check failed. Please start the server first:")
                print("   python main.py")
                return
        except:
            print("❌ Cannot connect to server. Please start the server first:")
            print("   python main.py")
            return
        
        print("✅ Server is accessible. Starting performance tests...")
        
        # Run performance tests
        self.concurrent_requests_test(10)  # 10 concurrent requests
        self.load_test(3, 20)  # 3 req/s for 20 seconds
        
        # Analyze results
        self.response_time_analysis()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print performance test summary"""
        print("\n" + "=" * 50)
        print("📊 PERFORMANCE TEST SUMMARY")
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
        
        if self.response_times:
            print(f"📊 Total Requests Tested: {len(self.response_times)}")
            print(f"⏱️  Average Response Time: {statistics.mean(self.response_times):.2f}s")

def main():
    """Main function to run performance tests"""
    print("🚀 CHATBOT PERFORMANCE TEST SUITE")
    print("=" * 50)
    print("This will test the chatbot's performance under load")
    print("Make sure the server is running: python main.py")
    print("=" * 50)
    
    # Run performance tests
    tester = PerformanceTester()
    tester.run_performance_suite()

if __name__ == "__main__":
    main()
