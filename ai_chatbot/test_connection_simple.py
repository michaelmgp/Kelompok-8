#!/usr/bin/env python3
"""
Simple test script to reproduce the connection race condition issue.
Uses only built-in Python libraries (urllib, json, time).
"""

import urllib.request
import urllib.parse
import json
import time
import threading
from typing import Dict, Any

class SimpleConnectionTest:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        
    def test_health(self) -> Dict[str, Any]:
        """Test the health endpoint"""
        try:
            url = f"{self.base_url}/health"
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return json.loads(response.read().decode())
                else:
                    return {"error": f"Health check failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Health check error: {str(e)}"}
    
    def test_agent_ready(self) -> Dict[str, Any]:
        """Test the agent ready endpoint"""
        try:
            url = f"{self.base_url}/agent/ready"
            with urllib.request.urlopen(url, timeout=5) as response:
                if response.status == 200:
                    return json.loads(response.read().decode())
                else:
                    return {"error": f"Agent ready failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Agent ready error: {str(e)}"}
    
    def test_chat(self, message: str) -> Dict[str, Any]:
        """Test the chat endpoint"""
        try:
            url = f"{self.base_url}/chat"
            payload = {"user_prompt": message, "top_k": 5}
            data = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    return json.loads(response.read().decode())
                else:
                    return {"error": f"Chat failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Chat error: {str(e)}"}
    
    def simulate_connection_check(self) -> Dict[str, Any]:
        """Simulate the frontend connection check"""
        try:
            print("🔍 Starting connection check...")
            start_time = time.time()
            
            # Test health endpoint
            health = self.test_health()
            if health.get("error"):
                return {"status": "failed", "error": health["error"], "duration": time.time() - start_time}
            
            # Test agent ready endpoint
            agent_ready = self.test_agent_ready()
            if agent_ready.get("error"):
                return {"status": "failed", "error": agent_ready["error"], "duration": time.time() - start_time}
            
            if agent_ready.get("ready"):
                duration = time.time() - start_time
                print(f"✅ Connection check completed in {duration:.3f}s")
                return {"status": "success", "message": "Connected to AI chatbot API", "duration": duration}
            else:
                duration = time.time() - start_time
                return {"status": "failed", "error": "AI agent is not ready", "duration": duration}
                
        except Exception as e:
            duration = time.time() - start_time
            return {"status": "failed", "error": f"Connection check error: {str(e)}", "duration": duration}
    
    def simulate_chat_request(self) -> Dict[str, Any]:
        """Simulate a chat request"""
        try:
            print("💬 Sending chat request...")
            start_time = time.time()
            
            result = self.test_chat("This is a test message")
            duration = time.time() - start_time
            
            if "error" not in result:
                print(f"✅ Chat request completed in {duration:.3f}s")
            else:
                print(f"❌ Chat request failed in {duration:.3f}s")
            
            return {"result": result, "duration": duration}
        except Exception as e:
            duration = time.time() - start_time
            return {"error": f"Chat request error: {str(e)}", "duration": duration}

def run_race_condition_test():
    """Run the race condition test"""
    print("🚀 Race Condition Test - Simple Version")
    print("=" * 60)
    
    tester = SimpleConnectionTest()
    
    # Test 1: Check if backend is running
    print("📡 Test 1: Backend Connectivity")
    print("-" * 30)
    
    health = tester.test_health()
    if health.get("error"):
        print(f"❌ Backend not accessible: {health['error']}")
        print("💡 Make sure to start the backend with: python main.py")
        return
    
    print(f"✅ Backend is accessible: {json.dumps(health, indent=2)}")
    
    # Test 2: Test agent endpoints
    print("\n🤖 Test 2: Agent Endpoints")
    print("-" * 30)
    
    agent_ready = tester.test_agent_ready()
    print(f"Agent Ready: {json.dumps(agent_ready, indent=2)}")
    
    # Test 3: Simulate race condition with threading
    print("\n🏁 Test 3: Race Condition Simulation")
    print("-" * 30)
    
    connection_result = None
    chat_result = None
    
    def run_connection_check():
        nonlocal connection_result
        connection_result = tester.simulate_connection_check()
    
    def run_chat_request():
        nonlocal chat_result
        chat_result = tester.simulate_chat_request()
    
    # Start both operations simultaneously
    print("🚀 Starting connection check and chat request simultaneously...")
    
    connection_thread = threading.Thread(target=run_connection_check)
    chat_thread = threading.Thread(target=run_chat_request)
    
    connection_thread.start()
    chat_thread.start()
    
    # Wait for both to complete
    connection_thread.join()
    chat_thread.join()
    
    # Test 4: Chat after connection is established
    print("\n💬 Test 4: Chat After Connection Established")
    print("-" * 30)
    
    # Wait a bit for connection to be fully established
    time.sleep(1)
    
    delayed_chat = tester.test_chat("This is a test message after connection is established")
    print(f"Delayed Chat: {json.dumps(delayed_chat, indent=2)}")
    
    # Analyze results
    print("\n📊 Test Analysis:")
    print("-" * 30)
    
    if connection_result and connection_result["status"] == "success":
        print(f"✅ Connection check: SUCCESS ({connection_result['duration']:.3f}s)")
    else:
        error_msg = connection_result["error"] if connection_result else "No result"
        print(f"❌ Connection check: FAILED - {error_msg}")
    
    if chat_result and "error" not in chat_result:
        print(f"✅ Immediate chat: SUCCESS ({chat_result['duration']:.3f}s)")
    else:
        error_msg = chat_result["error"] if chat_result else "No result"
        print(f"❌ Immediate chat: FAILED - {error_msg}")
    
    if "error" not in delayed_chat:
        print("✅ Delayed chat: SUCCESS")
    else:
        print(f"❌ Delayed chat: FAILED - {delayed_chat['error']}")
    
    # Identify the race condition
    if (connection_result and connection_result["status"] == "success" and 
        chat_result and "error" in chat_result and 
        "error" not in delayed_chat):
        print("\n🚨 RACE CONDITION DETECTED!")
        print("The immediate chat failed while the delayed chat succeeded.")
        print("This indicates a timing issue between connection check and chat requests.")
        print("\n💡 This is exactly what you're experiencing in the frontend!")
    else:
        print("\n✅ No race condition detected in this test run.")
        print("The issue might be more subtle or related to the frontend implementation.")

def main():
    """Main function"""
    try:
        run_race_condition_test()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
