#!/usr/bin/env python3
"""
Test script for the Explorer Agent

Simple test to verify the agent can be imported and initialized
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from core.config import get_settings
        print("✓ Configuration module imported")
        
        from core.agent import ExplorerAgent
        print("✓ Explorer Agent imported")
        
        from scrapers.base_scraper import BaseScraper
        print("✓ Base Scraper imported")
        
        from scrapers.linkedin_scraper import LinkedInScraper
        print("✓ LinkedIn Scraper imported")
        
        from processors.job_processor import JobProcessor
        print("✓ Job Processor imported")
        
        from streamers.websocket_manager import WebSocketManager
        print("✓ WebSocket Manager imported")
        
        from api.routes import router
        print("✓ API Routes imported")
        
        from models.job import JobListing
        print("✓ Job Models imported")
        
        from utils.helpers import clean_text, extract_skills_from_text
        print("✓ Utility functions imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

async def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from core.config import get_settings
        
        settings = get_settings()
        print(f"✓ Configuration loaded")
        print(f"  - Port: {settings.port}")
        print(f"  - Host: {settings.host}")
        print(f"  - Debug: {settings.debug}")
        print(f"  - Rate Limit: {settings.rate_limit}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def test_agent_creation():
    """Test agent creation"""
    print("\nTesting agent creation...")
    
    try:
        from core.agent import ExplorerAgent
        
        agent = ExplorerAgent()
        print("✓ Explorer Agent instance created")
        
        # Test initialization (without actual network calls)
        print("✓ Agent creation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Agent creation test failed: {e}")
        return False

async def test_utility_functions():
    """Test utility functions"""
    print("\nTesting utility functions...")
    
    try:
        from utils.helpers import clean_text, extract_skills_from_text, categorize_job
        
        # Test text cleaning
        test_text = "<p>This is a <strong>test</strong> text with   extra   spaces.</p>"
        cleaned = clean_text(test_text)
        expected = "This is a test text with extra spaces."
        assert cleaned == expected, f"Text cleaning failed: expected '{expected}', got '{cleaned}'"
        print("✓ Text cleaning works")
        
        # Test skill extraction
        test_description = "We are looking for a Python developer with React experience"
        skills = extract_skills_from_text(test_description)
        assert "Python" in skills, "Python skill not extracted"
        assert "React" in skills, "React skill not extracted"
        print("✓ Skill extraction works")
        
        # Test job categorization
        category = categorize_job("Senior Python Developer")
        assert category == "Software Development", f"Job categorization failed: expected 'Software Development', got '{category}'"
        print("✓ Job categorization works")
        
        print("✅ All utility function tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Utility function test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Explorer Agent Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_configuration,
        test_agent_creation,
        test_utility_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Explorer Agent is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

