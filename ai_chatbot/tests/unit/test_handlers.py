#!/usr/bin/env python3
"""
Unit Tests for Chatbot Handlers
Testing individual functions in isolation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from unittest.mock import Mock, patch
from chatbot.handlers import (
    parse_filters_with_profile,
    _extract_fallback_filters,
    Filters
)

class TestFilters:
    """Test Filters model validation"""
    
    def test_filters_creation(self):
        """Test creating Filters with valid data"""
        filters = Filters(
            skills=["java", "python"],
            location="New York",
            remote=True,
            experience_level="senior",
            budget_min=5000,
            budget_max=10000,
            rate_type="monthly",
            top_k=5
        )
        
        assert filters.skills == ["java", "python"]
        assert filters.location == "New York"
        assert filters.remote is True
        assert filters.experience_level == "senior"
        assert filters.budget_min == 5000
        assert filters.budget_max == 10000
        assert filters.rate_type == "monthly"
        assert filters.top_k == 5
    
    def test_filters_defaults(self):
        """Test Filters with minimal data"""
        filters = Filters(skills=["java"])
        
        assert filters.skills == ["java"]
        assert filters.location is None
        assert filters.remote is None
        assert filters.experience_level is None
        assert filters.budget_min is None
        assert filters.budget_max is None
        assert filters.rate_type is None
        assert filters.top_k == 5

class TestFallbackFilters:
    """Test fallback filter extraction"""
    
    def test_extract_skills(self):
        """Test skill extraction from various formats"""
        prompt = "Find me Java developer with Spring Boot and Docker experience"
        filters = _extract_fallback_filters(prompt)
        
        assert "java" in filters.skills
        assert "spring" in filters.skills
        assert "docker" in filters.skills
    
    def test_extract_salary_range(self):
        """Test salary range extraction"""
        prompt = "Looking for jobs with salary 5000-8000 USD per month"
        filters = _extract_fallback_filters(prompt)
        
        assert filters.budget_min == 5000
        assert filters.budget_max == 8000
        assert filters.rate_type == "monthly"
    
    def test_extract_location(self):
        """Test location extraction"""
        prompt = "Find remote jobs in New York or San Francisco"
        filters = _extract_fallback_filters(prompt)
        
        assert "new york" in filters.location.lower()
        assert "san francisco" in filters.location.lower()
        assert filters.remote is True
    
    def test_extract_experience_level(self):
        """Test experience level extraction"""
        prompt = "Need senior developer with 5+ years experience"
        filters = _extract_fallback_filters(prompt)
        
        assert filters.experience_level == "senior"
    
    def test_extract_top_k(self):
        """Test top_k extraction"""
        prompt = "Show me 10 best jobs for Python developers"
        filters = _extract_fallback_filters(prompt)
        
        assert filters.top_k == 10
    
    def test_complex_prompt(self):
        """Test complex prompt with multiple filters"""
        prompt = """
        I need a senior Java developer position with microservices experience, 
        remote work preferred, salary 8000-12000 USD/month, 
        show me top 15 results
        """
        filters = _extract_fallback_filters(prompt)
        
        assert "java" in filters.skills
        assert "microservices" in filters.skills
        assert filters.experience_level == "senior"
        assert filters.remote is True
        assert filters.budget_min == 8000
        assert filters.budget_max == 12000
        assert filters.rate_type == "monthly"
        assert filters.top_k == 15

class TestParseFiltersWithProfile:
    """Test filter parsing with user profile integration"""
    
    def test_parse_with_profile(self):
        """Test parsing filters when user profile is available"""
        user_profile = Mock()
        user_profile.skills = ["python", "django", "flask"]
        user_profile.location = "San Francisco"
        user_profile.experience_level = "mid"
        
        prompt = "Find me developer jobs"
        
        with patch('chatbot.handlers._extract_fallback_filters') as mock_extract:
            mock_extract.return_value = Filters(skills=["developer"])
            
            result = parse_filters_with_profile(prompt, user_profile)
            
            assert result is not None
            mock_extract.assert_called_once()
    
    def test_parse_without_profile(self):
        """Test parsing filters when no user profile"""
        prompt = "Find me Java developer jobs"
        
        with patch('chatbot.handlers._extract_fallback_filters') as mock_extract:
            mock_extract.return_value = Filters(skills=["java"])
            
            result = parse_filters_with_profile(prompt, None)
            
            assert result is not None
            mock_extract.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
