#!/usr/bin/env python3
"""
Quick Test Script for Individual Chatbot Testing
Simple tests for specific functionality
"""

import requests
import json
from datetime import datetime

def test_health():
    """Quick health check"""
    print("🏥 Testing Server Health...")
    try:
        response = requests.get("http://localhost:8081/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server healthy - {data.get('status')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect: {e}")
        return False

def test_basic_chat():
    """Quick basic chat test"""
    print("\n💬 Testing Basic Chat...")
    try:
        response = requests.post(
            "http://localhost:8081/chat",
            json={
                "user_prompt": "Find me Java developer jobs remote work",
                "user_principal": "quick_test_user",
                "top_k": 3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat response received")
            print(f"   Reply length: {len(data.get('reply', ''))} chars")
            print(f"   Filters: {data.get('filters', {})}")
            return True
        else:
            print(f"❌ Chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_profile():
    """Quick user profile test"""
    print("\n👤 Testing User Profile...")
    try:
        user_data = {
            "name": "Quick Test User",
            "email": "quick@test.com",
            "bio": "Quick test for profile creation",
            "skills": ["python", "testing"],
            "portfolio_url": "https://github.com/quicktest",
            "location": "Test City",
            "experience_level": "mid"
        }
        
        response = requests.post(
            "http://localhost:8081/user/profile?user_principal=quick_test_123",
            json=user_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Profile created: {data.get('profile_id')}")
            return True
        else:
            print(f"❌ Profile creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_personalized_chat():
    """Quick personalized chat test"""
    print("\n🎯 Testing Personalized Chat...")
    try:
        response = requests.post(
            "http://localhost:8081/chat/personalized",
            json={
                "user_prompt": "Find me Python developer jobs",
                "user_principal": "quick_test_123",
                "top_k": 3
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Personalized response received")
            print(f"   Personalized: {data.get('personalized', False)}")
            if data.get('user_profile'):
                profile = data['user_profile']
                print(f"   User: {profile.get('name', 'Unknown')}")
                print(f"   Skills: {', '.join(profile.get('skills', []))}")
            return True
        else:
            print(f"❌ Personalized chat failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run quick tests"""
    print("🧪 QUICK CHATBOT TESTS")
    print("=" * 40)
    print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 40)
    
    # Check server first
    if not test_health():
        print("\n❌ Server not accessible. Please start the server:")
        print("   python main.py")
        return
    
    # Run quick tests
    tests = [
        ("Basic Chat", test_basic_chat),
        ("User Profile", test_user_profile),
        ("Personalized Chat", test_personalized_chat)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 QUICK TEST RESULTS")
    print("=" * 40)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All quick tests passed!")
    else:
        print("💡 Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()
