#!/usr/bin/env python3
"""
Test script to reproduce the connection race condition issue.
This script simulates what happens in the frontend when a user tries to chat
before the connection check completes.
"""

import asyncio
import aiohttp
import time
import json
from typing import Dict, Any

class ConnectionRaceTest:
    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_health(self) -> Dict[str, Any]:
        """Test the health endpoint"""
        try:
            async with self.session.get(f"{self.base_url}/health") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Health check failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Health check error: {str(e)}"}
    
    async def test_agent_status(self) -> Dict[str, Any]:
        """Test the agent status endpoint"""
        try:
            async with self.session.get(f"{self.base_url}/agent/status") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Agent status failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Agent status error: {str(e)}"}
    
    async def test_agent_ready(self) -> Dict[str, Any]:
        """Test the agent ready endpoint"""
        try:
            async with self.session.get(f"{self.base_url}/agent/ready") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Agent ready failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Agent ready error: {str(e)}"}
    
    async def test_chat(self, message: str) -> Dict[str, Any]:
        """Test the chat endpoint"""
        try:
            payload = {"user_prompt": message, "top_k": 5}
            async with self.session.post(f"{self.base_url}/chat", json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Chat failed with status {response.status}"}
        except Exception as e:
            return {"error": f"Chat error: {str(e)}"}
    
    async def simulate_race_condition(self):
        """Simulate the race condition: connection check + immediate chat"""
        print("🚀 Starting Race Condition Test...")
        print("=" * 60)
        
        # Test 1: Basic connectivity
        print("📡 Test 1: Basic Connectivity")
        print("-" * 30)
        
        health_result = await self.test_health()
        print(f"Health Check: {json.dumps(health_result, indent=2)}")
        
        # Test 2: Agent endpoints
        print("\n🤖 Test 2: Agent Endpoints")
        print("-" * 30)
        
        agent_status = await self.test_agent_status()
        print(f"Agent Status: {json.dumps(agent_status, indent=2)}")
        
        agent_ready = await self.test_agent_ready()
        print(f"Agent Ready: {json.dumps(agent_ready, indent=2)}")
        
        # Test 3: Simulate race condition
        print("\n🏁 Test 3: Race Condition Simulation")
        print("-" * 30)
        
        # Start connection check (simulating frontend useEffect)
        print("Starting connection check...")
        connection_task = asyncio.create_task(self._simulate_connection_check())
        
        # Immediately try to chat (simulating user typing before connection completes)
        print("Immediately trying to chat...")
        chat_task = asyncio.create_task(self._simulate_chat_request())
        
        # Wait for both to complete
        connection_result, chat_result = await asyncio.gather(connection_task, chat_task)
        
        print(f"Connection Check Result: {connection_result}")
        print(f"Chat Request Result: {chat_result}")
        
        # Test 4: Chat after connection is established
        print("\n💬 Test 4: Chat After Connection Established")
        print("-" * 30)
        
        # Wait a bit for connection to be fully established
        await asyncio.sleep(1)
        
        delayed_chat = await self.test_chat("This is a test message after connection is established")
        print(f"Delayed Chat Result: {json.dumps(delayed_chat, indent=2)}")
        
        print("\n" + "=" * 60)
        print("🏁 Race Condition Test Complete!")
        
        return {
            "connection_result": connection_result,
            "immediate_chat_result": chat_result,
            "delayed_chat_result": delayed_chat
        }
    
    async def _simulate_connection_check(self) -> Dict[str, Any]:
        """Simulate the frontend connection check"""
        try:
            # Simulate the frontend's testConnection() method
            health = await self.test_health()
            if health.get("error"):
                return {"status": "failed", "error": health["error"]}
            
            agent_ready = await self.test_agent_ready()
            if agent_ready.get("error"):
                return {"status": "failed", "error": agent_ready["error"]}
            
            if agent_ready.get("ready"):
                return {"status": "success", "message": "Connected to AI chatbot API"}
            else:
                return {"status": "failed", "error": "AI agent is not ready"}
                
        except Exception as e:
            return {"status": "failed", "error": f"Connection check error: {str(e)}"}
    
    async def _simulate_chat_request(self) -> Dict[str, Any]:
        """Simulate an immediate chat request"""
        try:
            return await self.test_chat("This is a test message sent immediately")
        except Exception as e:
            return {"error": f"Immediate chat error: {str(e)}"}

async def main():
    """Main test function"""
    print("🔍 Connection Race Condition Test Script")
    print("This script tests the race condition between connection checking and chat requests")
    print("=" * 60)
    
    # Check if backend is running
    print("📡 Checking if backend is accessible...")
    
    async with ConnectionRaceTest() as tester:
        try:
            # Test basic connectivity first
            health = await tester.test_health()
            if health.get("error"):
                print(f"❌ Backend not accessible: {health['error']}")
                print("💡 Make sure to start the backend with: python main.py")
                return
            
            print("✅ Backend is accessible, running tests...")
            
            # Run the race condition test
            results = await tester.simulate_race_condition()
            
            # Analyze results
            print("\n📊 Test Analysis:")
            print("-" * 30)
            
            if results["connection_result"]["status"] == "success":
                print("✅ Connection check: SUCCESS")
            else:
                print(f"❌ Connection check: FAILED - {results['connection_result']['error']}")
            
            if "error" not in results["immediate_chat_result"]:
                print("✅ Immediate chat: SUCCESS")
            else:
                print(f"❌ Immediate chat: FAILED - {results['immediate_chat_result']['error']}")
            
            if "error" not in results["delayed_chat_result"]:
                print("✅ Delayed chat: SUCCESS")
            else:
                print(f"❌ Delayed chat: FAILED - {results['delayed_chat_result']['error']}")
            
            # Identify the race condition
            if (results["connection_result"]["status"] == "success" and 
                "error" in results["immediate_chat_result"] and 
                "error" not in results["delayed_chat_result"]):
                print("\n🚨 RACE CONDITION DETECTED!")
                print("The immediate chat failed while the delayed chat succeeded.")
                print("This indicates a timing issue between connection check and chat requests.")
            
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
