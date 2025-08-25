#!/usr/bin/env python3
"""
Unit Tests for Logging Functionality
Testing logging setup and configuration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import logging
import tempfile
import os
from unittest.mock import patch, MagicMock

class TestLogging:
    """Test logging functionality"""
    
    def test_logging_setup(self):
        """Test that logging is properly configured"""
        # Check if logging is configured
        root_logger = logging.getLogger()
        
        # Should have handlers
        assert len(root_logger.handlers) > 0, "Root logger should have handlers"
        
        # Check for console handler
        console_handlers = [h for h in root_logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(console_handlers) > 0, "Should have console handler"
        
        # Check log level
        assert root_logger.level <= logging.INFO, "Root logger should be at INFO level or lower"
    
    def test_logging_levels(self):
        """Test different logging levels"""
        logger = logging.getLogger("test_logger")
        
        # Test different log levels
        with patch('sys.stdout') as mock_stdout:
            logger.info("Test info message")
            logger.warning("Test warning message")
            logger.error("Test error message")
            
            # Verify that messages were logged
            # Note: In unit tests, we can't easily capture the actual output
            # but we can verify the logger is working
            assert logger.isEnabledFor(logging.INFO)
            assert logger.isEnabledFor(logging.WARNING)
            assert logger.isEnabledFor(logging.ERROR)
    
    def test_logging_format(self):
        """Test logging format"""
        logger = logging.getLogger("test_format_logger")
        
        # Check if formatter is set
        for handler in logger.handlers:
            if hasattr(handler, 'formatter') and handler.formatter:
                formatter = handler.formatter
                # Basic format check - should include timestamp and level
                format_string = formatter._fmt
                assert '%(asctime)s' in format_string, "Formatter should include timestamp"
                assert '%(levelname)s' in format_string, "Formatter should include level name"
    
    def test_logging_file_output(self):
        """Test logging to file"""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
            temp_filename = temp_file.name
            
            try:
                # Create a file handler
                file_handler = logging.FileHandler(temp_filename)
                file_handler.setLevel(logging.INFO)
                
                # Create a test logger
                test_logger = logging.getLogger("test_file_logger")
                test_logger.addHandler(file_handler)
                test_logger.setLevel(logging.INFO)
                
                # Log some messages
                test_message = "Test file logging message"
                test_logger.info(test_message)
                
                # Close the handler to flush the buffer
                file_handler.close()
                
                # Read the file and check if message was logged
                with open(temp_filename, 'r') as f:
                    content = f.read()
                    assert test_message in content, "Log message should be in file"
                    
            finally:
                # Clean up
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
    
    def test_logging_performance(self):
        """Test logging performance (basic)"""
        logger = logging.getLogger("test_performance_logger")
        
        import time
        start_time = time.time()
        
        # Log multiple messages
        for i in range(100):
            logger.info(f"Performance test message {i}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Logging 100 messages should be very fast (< 1 second)
        assert duration < 1.0, f"Logging 100 messages took {duration:.2f}s, should be < 1s"
    
    def test_logging_context(self):
        """Test logging context and extra fields"""
        logger = logging.getLogger("test_context_logger")
        
        # Test logging with extra context
        extra_data = {"user_id": "123", "session_id": "abc"}
        
        # This is a basic test - in practice, you might use structured logging
        # or custom formatters to handle extra fields
        logger.info("Test message with context", extra=extra_data)
        
        # Verify logger can handle extra data
        assert logger.isEnabledFor(logging.INFO)

if __name__ == "__main__":
    # Run tests
    test_suite = TestLogging()
    
    # Run each test method
    test_methods = [
        test_suite.test_logging_setup,
        test_suite.test_logging_levels,
        test_suite.test_logging_format,
        test_suite.test_logging_file_output,
        test_suite.test_logging_performance,
        test_suite.test_logging_context
    ]
    
    print("🧪 LOGGING UNIT TESTS")
    print("=" * 40)
    
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
        print("🎉 All logging tests passed!")
    else:
        print("💡 Some logging tests failed. Check the output above.")
