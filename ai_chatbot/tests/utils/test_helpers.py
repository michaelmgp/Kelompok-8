#!/usr/bin/env python3
"""
Test Helper Utilities
Common test data and helper functions for all test types
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from datetime import datetime
from typing import Dict, List, Any

class TestData:
    """Common test data for all test types"""
    
    # Sample user profiles for testing
    SAMPLE_USERS = {
        "java_senior": {
            "principal": "alice_java_123",
            "name": "Alice Java Developer",
            "email": "alice@java.dev",
            "bio": "Senior Java developer with 8+ years experience",
            "skills": ["java", "spring", "microservices", "docker", "kubernetes"],
            "portfolio_url": "https://github.com/alicejava",
            "location": "San Francisco, CA",
            "experience_level": "senior",
            "verification_status": "Verified",
            "reputation_score": 4.8
        },
        "react_mid": {
            "principal": "bob_react_456",
            "name": "Bob React Developer",
            "email": "bob@react.dev",
            "bio": "Mid-level React developer with 3 years experience",
            "skills": ["react", "typescript", "javascript", "node.js", "css"],
            "portfolio_url": "https://github.com/bobreact",
            "location": "New York, NY",
            "experience_level": "mid",
            "verification_status": "Verified",
            "reputation_score": 4.2
        },
        "python_junior": {
            "principal": "carol_python_789",
            "name": "Carol Python Developer",
            "email": "carol@python.dev",
            "bio": "Junior Python developer eager to learn",
            "skills": ["python", "django", "flask", "sql", "git"],
            "portfolio_url": "https://github.com/carolpython",
            "location": "Austin, TX",
            "experience_level": "junior",
            "verification_status": "Pending",
            "reputation_score": 3.5
        }
    }
    
    # Sample job search prompts for testing
    SAMPLE_PROMPTS = {
        "basic": [
            "Find me Java developer jobs",
            "Show Python developer positions",
            "Looking for React developer roles"
        ],
        "detailed": [
            "I need a senior Java developer with microservices experience, remote work, salary 8000-12000 USD/month",
            "Looking for React developer with TypeScript, 3+ years experience, hybrid work in NYC, budget 6000-9000 USD/month",
            "Python developer needed for machine learning projects, entry level, remote work preferred, salary 3000-5000 USD/month"
        ],
        "complex": [
            "Find me a senior full-stack developer with Java backend and React frontend experience, must have Docker and AWS knowledge, remote work only, salary range 10000-15000 USD per month, show me top 20 results",
            "Looking for a mid-level DevOps engineer with Kubernetes experience, hybrid work in San Francisco or New York, must know Python and Go, salary 7000-10000 USD monthly, need someone who can start immediately"
        ]
    }
    
    # Sample filter results for testing
    SAMPLE_FILTERS = {
        "java_remote": {
            "skills": ["java"],
            "remote": True,
            "location": None,
            "experience_level": None,
            "budget_min": None,
            "budget_max": None,
            "rate_type": None,
            "top_k": 5
        },
        "python_senior_nyc": {
            "skills": ["python"],
            "remote": False,
            "location": "New York",
            "experience_level": "senior",
            "budget_min": None,
            "budget_max": None,
            "rate_type": None,
            "top_k": 5
        },
        "full_stack_budget": {
            "skills": ["javascript", "python", "react", "node.js"],
            "remote": True,
            "location": None,
            "experience_level": "mid",
            "budget_min": 6000,
            "budget_max": 10000,
            "rate_type": "monthly",
            "top_k": 10
        }
    }

class TestHelpers:
    """Helper functions for testing"""
    
    @staticmethod
    def create_mock_user_profile(user_type: str = "java_senior") -> Dict[str, Any]:
        """Create a mock user profile for testing"""
        if user_type in TestData.SAMPLE_USERS:
            return TestData.SAMPLE_USERS[user_type].copy()
        else:
            return TestData.SAMPLE_USERS["java_senior"].copy()
    
    @staticmethod
    def create_mock_filters(filter_type: str = "java_remote") -> Dict[str, Any]:
        """Create mock filters for testing"""
        if filter_type in TestData.SAMPLE_FILTERS:
            return TestData.SAMPLE_FILTERS[filter_type].copy()
        else:
            return TestData.SAMPLE_FILTERS["java_remote"].copy()
    
    @staticmethod
    def generate_test_prompt(prompt_type: str = "basic", index: int = 0) -> str:
        """Generate a test prompt for testing"""
        if prompt_type in TestData.SAMPLE_PROMPTS:
            prompts = TestData.SAMPLE_PROMPTS[prompt_type]
            if 0 <= index < len(prompts):
                return prompts[index]
        return "Find me developer jobs"  # Default fallback
    
    @staticmethod
    def validate_response_structure(response: Dict[str, Any]) -> bool:
        """Validate that response has required structure"""
        required_fields = ["reply", "filters", "personalized"]
        
        for field in required_fields:
            if field not in response:
                return False
        
        return True
    
    @staticmethod
    def validate_filters_structure(filters: Dict[str, Any]) -> bool:
        """Validate that filters have required structure"""
        required_fields = [
            "skills", "remote", "location", "experience_level",
            "budget_min", "budget_max", "rate_type", "top_k"
        ]
        
        for field in required_fields:
            if field not in filters:
                return False
        
        return True
    
    @staticmethod
    def calculate_response_time(start_time: float, end_time: float) -> float:
        """Calculate response time in seconds"""
        return end_time - start_time
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration in human-readable format"""
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.2f}s"
        else:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds:.1f}s"
    
    @staticmethod
    def generate_test_report(test_name: str, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a test report from results"""
        total_tests = len(results)
        passed_tests = len([r for r in results if r.get("status") == "PASS"])
        failed_tests = len([r for r in results if r.get("status") == "FAIL"])
        warning_tests = len([r for r in results if r.get("status") == "WARNING"])
        
        return {
            "test_suite": test_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "warning_tests": warning_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "results": results
        }

class MockResponses:
    """Mock response objects for testing"""
    
    @staticmethod
    def mock_success_response(data: Dict[str, Any] = None) -> Mock:
        """Create a mock successful response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = data or {
            "status": "success",
            "message": "Test response"
        }
        mock_response.text = "Success response"
        return mock_response
    
    @staticmethod
    def mock_error_response(status_code: int = 400, error_message: str = "Bad Request") -> Mock:
        """Create a mock error response"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = {
            "error": error_message,
            "status_code": status_code
        }
        mock_response.text = error_message
        return mock_response
    
    @staticmethod
    def mock_connection_error() -> Mock:
        """Create a mock connection error"""
        mock_response = Mock()
        mock_response.side_effect = Exception("Connection refused")
        return mock_response

# Export commonly used items
__all__ = [
    'TestData',
    'TestHelpers', 
    'MockResponses'
]
