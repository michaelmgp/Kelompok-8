#!/usr/bin/env python3
"""
Unit Tests for Chatbot Models
Testing LLM initialization and configuration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from unittest.mock import Mock, patch
from chatbot.model import LLM

class TestLLM:
    """Test LLM model initialization and configuration"""
    
    @patch('chatbot.model.os.getenv')
    def test_grok_initialization(self, mock_getenv):
        """Test Grok model initialization"""
        mock_getenv.side_effect = lambda key, default=None: {
            'MODEL_TYPE': 'grok',
            'GROK_API_KEY': 'test_grok_key'
        }.get(key, default)
        
        llm = LLM()
        
        assert llm.model_type == 'grok'
        assert llm.api_key == 'test_grok_key'
    
    @patch('chatbot.model.os.getenv')
    def test_openai_initialization(self, mock_getenv):
        """Test OpenAI model initialization"""
        mock_getenv.side_effect = lambda key, default=None: {
            'MODEL_TYPE': 'openai',
            'OPENAI_API_KEY': 'test_openai_key'
        }.get(key, default)
        
        llm = LLM()
        
        assert llm.model_type == 'openai'
        assert llm.api_key == 'test_openai_key'
    
    @patch('chatbot.model.os.getenv')
    def test_default_model_type(self, mock_getenv):
        """Test default model type when not specified"""
        mock_getenv.side_effect = lambda key, default=None: {
            'GROK_API_KEY': 'test_key'
        }.get(key, default)
        
        llm = LLM()
        
        assert llm.model_type == 'grok'  # Default should be grok
    
    @patch('chatbot.model.os.getenv')
    def test_missing_api_key(self, mock_getenv):
        """Test behavior when API key is missing"""
        mock_getenv.side_effect = lambda key, default=None: {
            'MODEL_TYPE': 'grok'
        }.get(key, default)
        
        with pytest.raises(ValueError, match="API key not found"):
            LLM()
    
    @patch('chatbot.model.os.getenv')
    def test_invalid_model_type(self, mock_getenv):
        """Test behavior with invalid model type"""
        mock_getenv.side_effect = lambda key, default=None: {
            'MODEL_TYPE': 'invalid_model',
            'GROK_API_KEY': 'test_key'
        }.get(key, default)
        
        with pytest.raises(ValueError, match="Unsupported model type"):
            LLM()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
