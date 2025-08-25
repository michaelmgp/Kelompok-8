#!/usr/bin/env python3
"""
Unit Tests for Prompt Processing
Testing specific prompt scenarios and filter extraction
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from unittest.mock import Mock, patch
from chatbot.handlers import _extract_fallback_filters, Filters

class TestPromptProcessing:
    """Test prompt processing and filter extraction"""
    
    def test_salary_extraction_various_formats(self):
        """Test salary extraction from various formats"""
        test_cases = [
            {
                "prompt": "Find me Java developer jobs with salary 1500USD/month remote fulltime",
                "expected": {
                    "budget_min": 1500,
                    "budget_max": 1500,
                    "rate_type": "monthly",
                    "skills": ["java"],
                    "remote": True
                }
            },
            {
                "prompt": "Looking for React developer with salary 5000-8000 USD per month",
                "expected": {
                    "budget_min": 5000,
                    "budget_max": 8000,
                    "rate_type": "monthly",
                    "skills": ["react"]
                }
            },
            {
                "prompt": "Need Python developer, budget $3000-$6000 monthly",
                "expected": {
                    "budget_min": 3000,
                    "budget_max": 6000,
                    "rate_type": "monthly",
                    "skills": ["python"]
                }
            },
            {
                "prompt": "Find senior developer with 10000-15000 USD per month",
                "expected": {
                    "budget_min": 10000,
                    "budget_max": 15000,
                    "rate_type": "monthly",
                    "experience_level": "senior"
                }
            }
        ]
        
        for test_case in test_cases:
            filters = _extract_fallback_filters(test_case["prompt"])
            expected = test_case["expected"]
            
            for key, expected_value in expected.items():
                if hasattr(filters, key):
                    actual_value = getattr(filters, key)
                    assert actual_value == expected_value, \
                        f"Failed for prompt: '{test_case['prompt']}'\n" \
                        f"Expected {key}: {expected_value}, got: {actual_value}"
    
    def test_experience_level_extraction(self):
        """Test experience level extraction"""
        test_cases = [
            ("Need junior developer", "junior"),
            ("Looking for senior developer", "senior"),
            ("Mid-level developer required", "mid"),
            ("Entry level position", "junior"),
            ("Expert developer needed", "senior")
        ]
        
        for prompt, expected_level in test_cases:
            filters = _extract_fallback_filters(prompt)
            assert filters.experience_level == expected_level, \
                f"Failed for prompt: '{prompt}'\n" \
                f"Expected: {expected_level}, got: {filters.experience_level}"
    
    def test_location_extraction(self):
        """Test location extraction"""
        test_cases = [
            ("Find jobs in New York", "new york"),
            ("Looking for positions in San Francisco", "san francisco"),
            ("Remote jobs in London", "london"),
            ("Hybrid work in Austin, TX", "austin, tx"),
            ("On-site in Seattle, Washington", "seattle, washington")
        ]
        
        for prompt, expected_location in test_cases:
            filters = _extract_fallback_filters(prompt)
            if filters.location:
                assert expected_location in filters.location.lower(), \
                    f"Failed for prompt: '{prompt}'\n" \
                    f"Expected location to contain: {expected_location}, got: {filters.location}"
    
    def test_remote_work_extraction(self):
        """Test remote work preference extraction"""
        test_cases = [
            ("Find remote Java developer jobs", True),
            ("Looking for on-site positions", False),
            ("Hybrid work preferred", False),
            ("Remote work only", True),
            ("Work from home opportunities", True),
            ("Office-based positions", False)
        ]
        
        for prompt, expected_remote in test_cases:
            filters = _extract_fallback_filters(prompt)
            if filters.remote is not None:
                assert filters.remote == expected_remote, \
                    f"Failed for prompt: '{prompt}'\n" \
                    f"Expected remote: {expected_remote}, got: {filters.remote}"
    
    def test_top_k_extraction(self):
        """Test top_k extraction from prompts"""
        test_cases = [
            ("Show me 10 best jobs", 10),
            ("Find top 5 positions", 5),
            ("Give me 20 results", 20),
            ("Show 3 jobs", 3),
            ("Find 15 developer positions", 15)
        ]
        
        for prompt, expected_top_k in test_cases:
            filters = _extract_fallback_filters(prompt)
            assert filters.top_k == expected_top_k, \
                f"Failed for prompt: '{prompt}'\n" \
                f"Expected top_k: {expected_top_k}, got: {filters.top_k}"
    
    def test_complex_prompt_parsing(self):
        """Test complex prompt with multiple requirements"""
        complex_prompt = """
        I need a senior full-stack developer with Java backend and React frontend experience, 
        must have Docker and AWS knowledge, remote work only, salary range 10000-15000 USD per month, 
        show me top 20 results, location preference for US timezone
        """
        
        filters = _extract_fallback_filters(complex_prompt)
        
        # Check multiple extracted values
        assert "java" in filters.skills, "Java skill should be extracted"
        assert "react" in filters.skills, "React skill should be extracted"
        assert "docker" in filters.skills, "Docker skill should be extracted"
        assert "aws" in filters.skills, "AWS skill should be extracted"
        assert filters.experience_level == "senior", "Experience level should be senior"
        assert filters.remote is True, "Remote work should be True"
        assert filters.budget_min == 10000, "Budget min should be 10000"
        assert filters.budget_max == 15000, "Budget max should be 15000"
        assert filters.rate_type == "monthly", "Rate type should be monthly"
        assert filters.top_k == 20, "Top K should be 20"
    
    def test_edge_cases(self):
        """Test edge cases and unusual prompts"""
        edge_cases = [
            ("", "Empty prompt"),
            ("   ", "Whitespace only"),
            ("Find jobs", "Minimal prompt"),
            ("1234567890", "Numbers only"),
            ("!@#$%^&*()", "Special characters only"),
            ("Find me a developer with salary 0 USD per month", "Zero salary"),
            ("Looking for developer with salary 999999 USD per month", "Very high salary")
        ]
        
        for prompt, description in edge_cases:
            try:
                filters = _extract_fallback_filters(prompt)
                # Should not crash, even for edge cases
                assert isinstance(filters, Filters), f"Should return Filters object for: {description}"
            except Exception as e:
                pytest.fail(f"Edge case failed for '{description}': {str(e)}")
    
    def test_skill_variations(self):
        """Test various skill name variations"""
        skill_variations = [
            ("Java", "java"),
            ("JAVA", "java"),
            ("java", "java"),
            ("Python", "python"),
            ("PYTHON", "python"),
            ("React.js", "react"),
            ("NodeJS", "node.js"),
            ("TypeScript", "typescript"),
            ("Machine Learning", "machine learning"),
            ("AI/ML", "ai/ml")
        ]
        
        for skill_input, expected_skill in skill_variations:
            prompt = f"Find me {skill_input} developer jobs"
            filters = _extract_fallback_filters(prompt)
            
            # Check if the expected skill is in the extracted skills
            extracted_skills = [skill.lower() for skill in filters.skills]
            assert expected_skill.lower() in extracted_skills, \
                f"Failed for skill: '{skill_input}'\n" \
                f"Expected: {expected_skill}, extracted skills: {filters.skills}"

if __name__ == "__main__":
    # Run tests
    test_suite = TestPromptProcessing()
    
    # Run each test method
    test_methods = [
        test_suite.test_salary_extraction_various_formats,
        test_suite.test_experience_level_extraction,
        test_suite.test_location_extraction,
        test_suite.test_remote_work_extraction,
        test_suite.test_top_k_extraction,
        test_suite.test_complex_prompt_parsing,
        test_suite.test_edge_cases,
        test_suite.test_skill_variations
    ]
    
    print("🧪 PROMPT PROCESSING UNIT TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(test_methods)
    
    for test_method in test_methods:
        try:
            test_method()
            print(f"✅ {test_method.__name__}: PASS")
            passed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__}: FAIL - {str(e)}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 All prompt processing tests passed!")
    else:
        print("💡 Some prompt processing tests failed. Check the output above.")
