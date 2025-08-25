#!/usr/bin/env python3
"""
Test script for the specific prompt that was failing
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot.handlers import handle_chat, _extract_fallback_filters

def test_specific_prompt():
    """Test the specific prompt that was failing"""
    print("🚀 Testing Specific Prompt...")
    print("=" * 60)
    
    # The exact prompt that was failing
    test_prompt = "Hey Give me Java developer jobs full time remote with salary minimum 1500USD a month, give me 10 jobs"
    
    print(f"📝 Test prompt: {test_prompt}")
    print("-" * 40)
    
    # Test fallback parsing first
    print("🔍 Testing fallback filter extraction...")
    fallback_filters = _extract_fallback_filters(test_prompt)
    print(f"✅ Fallback filters: {fallback_filters}")
    
    print("\n🤖 Testing full chatbot processing...")
    try:
        result = handle_chat(test_prompt)
        print(f"✅ Chat result received!")
        print(f"📤 Message: {result.message}")
        print(f"🎯 Final filters: {result.filters.model_dump_json(indent=2)}")
        
        # Show what was extracted
        print("\n📊 Filter Summary:")
        print(f"   Skills: {result.filters.skills}")
        print(f"   Keywords: {result.filters.keywords}")
        print(f"   Budget: ${result.filters.budget_min} - ${result.filters.budget_max}")
        print(f"   Rate Type: {result.filters.rate_type}")
        print(f"   Remote: {result.filters.remote}")
        print(f"   Duration: {result.filters.duration_days_max} days")
        print(f"   Top K: {result.filters.top_k}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if Grok API key is set
    if not os.getenv("GROK_API_KEY"):
        print("❌ GROK_API_KEY not found in environment variables")
        print("Please set it in your .env file")
        sys.exit(1)
    
    print("🔑 Grok API key found")
    test_specific_prompt()
