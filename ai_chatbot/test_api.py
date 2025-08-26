#!/usr/bin/env python3
"""
Test script to test the API endpoints and see logging in action
Make sure the server is running first: python main.py
"""

import requests
import json
import time

def test_api_endpoints():
    """Test the chatbot API endpoints"""
    base_url = "http://localhost:8081"
    
    print("🚀 Testing Chatbot API Endpoints...")
    print("=" * 60)
    
    # Test health endpoint
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test chat endpoint
    print("\n💬 Testing chat endpoint...")
    test_prompts = [
        "Find me a Python developer job with React skills, budget around $5000",
        "I need a blockchain engineer for remote work, hourly rate $50-100"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: {prompt}")
        print("-" * 40)
        
        try:
            payload = {
                "user_prompt": prompt,
                "top_k": 5
            }
            
            response = requests.post(
                f"{base_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Chat response received!")
                print(f"📤 Message: {result['message']}")
                print(f"🎯 Filters: {json.dumps(result['filters'], indent=2)}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    # Test parse endpoint
    print("\n🔍 Testing parse endpoint...")
    try:
        payload = {
            "user_prompt": "Looking for AI/ML researcher, fixed project under $10000",
            "top_k": 3
        }
        
        response = requests.post(
            f"{base_url}/parse",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            filters = response.json()
            print(f"✅ Parse response received!")
            print(f"🎯 Parsed filters: {json.dumps(filters, indent=2)}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Parse request failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API testing completed!")

if __name__ == "__main__":
    print("🔧 Make sure the chatbot server is running first:")
    print("   cd ai_chatbot")
    print("   python main.py")
    print("\n" + "=" * 60)
    
    # Wait a moment for user to read
    input("Press Enter when the server is running...")
    
    test_api_endpoints()
