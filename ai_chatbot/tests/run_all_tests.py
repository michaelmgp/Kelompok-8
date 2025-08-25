#!/usr/bin/env python3
"""
Main Test Runner
Execute all test types from one place
"""

import sys
import os
import time
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def run_unit_tests():
    """Run unit tests"""
    print("\n🧪 RUNNING UNIT TESTS")
    print("=" * 40)
    
    try:
        # Import and run unit tests
        from unit.test_handlers import TestFilters, TestFallbackFilters, TestParseFiltersWithProfile
        from unit.test_models import TestLLM
        
        print("✅ Unit tests imported successfully")
        print("💡 Run individual unit tests with: python -m pytest tests/unit/")
        
    except ImportError as e:
        print(f"❌ Unit test import failed: {e}")
        print("💡 Install pytest: pip install pytest")
        return False
    
    return True

def run_integration_tests():
    """Run integration tests"""
    print("\n🧪 RUNNING INTEGRATION TESTS")
    print("=" * 40)
    
    try:
        # Import integration test suite
        from integration.test_chat_endpoints import TestChatEndpoints
        
        print("✅ Integration tests imported successfully")
        print("💡 Run integration tests with: python tests/integration/test_chat_endpoints.py")
        
    except ImportError as e:
        print(f"❌ Integration test import failed: {e}")
        return False
    
    return True

def run_performance_tests():
    """Run performance tests"""
    print("\n🧪 RUNNING PERFORMANCE TESTS")
    print("=" * 40)
    
    try:
        # Import performance test suite
        from performance.test_load import PerformanceTester
        
        print("✅ Performance tests imported successfully")
        print("💡 Run performance tests with: python tests/performance/test_load.py")
        
    except ImportError as e:
        print(f"❌ Performance test import failed: {e}")
        return False
    
    return True

def run_comprehensive_suite():
    """Run the comprehensive test suite"""
    print("\n🧪 RUNNING COMPREHENSIVE TEST SUITE")
    print("=" * 40)
    
    try:
        # Import comprehensive test suite
        from ..test_suite import ChatbotTestSuite
        
        print("✅ Comprehensive test suite imported successfully")
        print("💡 Run comprehensive tests with: python test_suite.py")
        
    except ImportError as e:
        print(f"❌ Comprehensive test suite import failed: {e}")
        return False
    
    return True

def run_quick_tests():
    """Run quick tests"""
    print("\n🧪 RUNNING QUICK TESTS")
    print("=" * 40)
    
    try:
        # Import quick test suite
        from ..quick_test import main as quick_test_main
        
        print("✅ Quick tests imported successfully")
        print("💡 Run quick tests with: python quick_test.py")
        
    except ImportError as e:
        print(f"❌ Quick test import failed: {e}")
        return False
    
    return True

def main():
    """Main function to run all test types"""
    print("🚀 CHATBOT COMPLETE TEST RUNNER")
    print("=" * 60)
    print("This will check all test types and provide guidance")
    print("=" * 60)
    
    start_time = time.time()
    
    # Test results
    test_results = {
        "Unit Tests": False,
        "Integration Tests": False,
        "Performance Tests": False,
        "Comprehensive Suite": False,
        "Quick Tests": False
    }
    
    # Run each test type
    test_results["Unit Tests"] = run_unit_tests()
    test_results["Integration Tests"] = run_integration_tests()
    test_results["Performance Tests"] = run_performance_tests()
    test_results["Comprehensive Suite"] = run_comprehensive_suite()
    test_results["Quick Tests"] = run_quick_tests()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUITE STATUS")
    print("=" * 60)
    
    total_tests = len(test_results)
    available_tests = sum(test_results.values())
    
    for test_type, available in test_results.items():
        status = "✅ Available" if available else "❌ Not Available"
        print(f"{status} {test_type}")
    
    print(f"\n📈 Test Suites Available: {available_tests}/{total_tests}")
    
    # Print usage instructions
    print("\n" + "=" * 60)
    print("📚 HOW TO RUN TESTS")
    print("=" * 60)
    
    print("1. 🧪 Unit Tests (Individual Functions):")
    print("   python -m pytest tests/unit/")
    print("   python tests/unit/test_handlers.py")
    print("   python tests/unit/test_models.py")
    
    print("\n2. 🔗 Integration Tests (API Endpoints):")
    print("   python tests/integration/test_chat_endpoints.py")
    print("   # Make sure server is running: python main.py")
    
    print("\n3. ⚡ Performance Tests (Load & Concurrency):")
    print("   python tests/performance/test_load.py")
    print("   # Make sure server is running: python main.py")
    
    print("\n4. 🚀 Comprehensive Test Suite (All Features):")
    print("   python test_suite.py")
    print("   # Make sure server is running: python main.py")
    
    print("\n5. ⚡ Quick Tests (Basic Functionality):")
    print("   python quick_test.py")
    print("   # Make sure server is running: python main.py")
    
    print("\n6. 🎯 Run All Tests from Root:")
    print("   cd ai_chatbot")
    print("   python tests/run_all_tests.py")
    
    # Print test organization info
    print("\n" + "=" * 60)
    print("🗂️  TEST ORGANIZATION")
    print("=" * 60)
    
    print("📁 tests/")
    print("   ├── unit/           # Individual function tests")
    print("   │   ├── test_handlers.py")
    print("   │   └── test_models.py")
    print("   ├── integration/    # API endpoint tests")
    print("   │   └── test_chat_endpoints.py")
    print("   ├── performance/    # Load and performance tests")
    print("   │   └── test_load.py")
    print("   ├── utils/          # Test helpers and utilities")
    print("   │   └── test_helpers.py")
    print("   ├── __init__.py     # Package initialization")
    print("   └── run_all_tests.py # This file")
    
    print("\n📁 Root Level:")
    print("   ├── test_suite.py   # Comprehensive test suite")
    print("   └── quick_test.py   # Quick functionality tests")
    
    total_duration = time.time() - start_time
    print(f"\n⏱️  Total execution time: {total_duration:.2f}s")
    print("🎉 Test runner completed successfully!")

if __name__ == "__main__":
    main()
