#!/usr/bin/env python3
"""
Test script to demonstrate the new logging functionality
This will show Grok responses and filtered results
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot.handlers import handle_chat

def test_chat_with_logging():
    """Test the chatbot with comprehensive logging"""
    print("🚀 Testing Chatbot with Logging...")
    print("=" * 60)
    
    # Test different types of prompts
    test_prompts = [
        "Find me a Python developer job with React skills, budget around $5000",
        "I need a blockchain engineer for remote work, hourly rate $50-100",
        "Looking for AI/ML researcher, fixed project under $10000, 2 months duration"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: {prompt}")
        print("-" * 40)
        
        try:
            result = handle_chat(prompt)
            print(f"✅ Chat result received!")
            print(f"📤 Message: {result.message}")
            print(f"🎯 Filters: {result.filters.model_dump_json(indent=2)}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
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
    test_chat_with_logging()
