"""
Chatbot Test Suite Package
Organized testing framework for all chatbot functionality
"""

__version__ = "1.0.0"
__author__ = "Chatbot Development Team"

# Import test utilities for easy access
from .utils.test_helpers import TestData, TestHelpers, MockResponses

__all__ = [
    'TestData',
    'TestHelpers', 
    'MockResponses'
]
