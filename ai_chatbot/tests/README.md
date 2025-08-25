# 🧪 Chatbot Test Suite

**Organized, comprehensive testing framework for all chatbot functionality**

## 📁 Test Organization

```
tests/
├── unit/                    # Individual function tests
│   ├── test_handlers.py    # Handler function tests
│   └── test_models.py      # LLM model tests
├── integration/             # API endpoint tests
│   └── test_chat_endpoints.py
├── performance/             # Load and performance tests
│   └── test_load.py
├── utils/                   # Test helpers and utilities
│   └── test_helpers.py
├── __init__.py             # Package initialization
├── run_all_tests.py        # Main test runner
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Check Test Status
```bash
cd ai_chatbot
python tests/run_all_tests.py
```

### 2. Run Specific Test Types

#### Unit Tests (Individual Functions)
```bash
# Run all unit tests
python -m pytest tests/unit/

# Run specific unit test
python tests/unit/test_handlers.py
python tests/unit/test_models.py
```

#### Integration Tests (API Endpoints)
```bash
# Start server first
python main.py

# In another terminal, run integration tests
python tests/integration/test_chat_endpoints.py
```

#### Performance Tests (Load & Concurrency)
```bash
# Start server first
python main.py

# In another terminal, run performance tests
python tests/performance/test_load.py
```

#### Comprehensive Test Suite (All Features)
```bash
# Start server first
python main.py

# In another terminal, run comprehensive tests
python test_suite.py
```

#### Quick Tests (Basic Functionality)
```bash
# Start server first
python main.py

# In another terminal, run quick tests
python quick_test.py
```

## 🧪 Test Types Explained

### 1. **Unit Tests** (`tests/unit/`)
- **Purpose**: Test individual functions in isolation
- **Scope**: Handler functions, model initialization, filter parsing
- **Dependencies**: Minimal, mostly mock objects
- **Speed**: Fast execution
- **Use Case**: Development, debugging, CI/CD

**Files:**
- `test_handlers.py` - Test filter extraction and parsing logic
- `test_models.py` - Test LLM model initialization and configuration

### 2. **Integration Tests** (`tests/integration/`)
- **Purpose**: Test API endpoints with running server
- **Scope**: HTTP endpoints, request/response cycles
- **Dependencies**: Running FastAPI server
- **Speed**: Medium execution (includes HTTP calls)
- **Use Case**: API validation, end-to-end functionality

**Files:**
- `test_chat_endpoints.py` - Test chat and user management endpoints

### 3. **Performance Tests** (`tests/performance/`)
- **Purpose**: Test system performance under load
- **Scope**: Response times, concurrent requests, sustained load
- **Dependencies**: Running server, network capacity
- **Speed**: Slow execution (load testing)
- **Use Case**: Performance validation, capacity planning

**Files:**
- `test_load.py` - Test concurrent requests and sustained load

### 4. **Utility Tests** (`tests/utils/`)
- **Purpose**: Provide common test data and helper functions
- **Scope**: Mock data, validation functions, test utilities
- **Dependencies**: None (standalone utilities)
- **Speed**: Instant (utility functions)
- **Use Case**: Shared across all test types

**Files:**
- `test_helpers.py` - Common test data, mock objects, validation functions

## 📊 Test Data & Utilities

### TestData Class
```python
from tests.utils.test_helpers import TestData

# Sample user profiles
user = TestData.SAMPLE_USERS["java_senior"]

# Sample prompts
prompt = TestData.SAMPLE_PROMPTS["detailed"][0]

# Sample filters
filters = TestData.SAMPLE_FILTERS["java_remote"]
```

### TestHelpers Class
```python
from tests.utils.test_helpers import TestHelpers

# Create mock user profile
profile = TestHelpers.create_mock_user_profile("react_mid")

# Validate response structure
is_valid = TestHelpers.validate_response_structure(response)

# Calculate response time
duration = TestHelpers.calculate_response_time(start, end)
```

### MockResponses Class
```python
from tests.utils.test_helpers import MockResponses

# Create mock success response
success_response = MockResponses.mock_success_response(data)

# Create mock error response
error_response = MockResponses.mock_error_response(400, "Bad Request")
```

## 🔧 Test Configuration

### Environment Setup
```bash
# Install test dependencies
pip install pytest requests python-dotenv

# Set up environment variables
cp env.example .env
# Edit .env with your API keys
```

### Running with Different Configurations
```bash
# Run with verbose output
python -m pytest tests/unit/ -v

# Run with coverage
python -m pytest tests/unit/ --cov=chatbot

# Run specific test function
python -m pytest tests/unit/test_handlers.py::TestFilters::test_filters_creation
```

## 📈 Test Results & Reporting

### Output Format
All tests provide structured output with:
- ✅/❌/⚠️ Status indicators
- 📝 Detailed information
- ⏱️ Timing information
- 📊 Summary statistics

### Result Files
- **JSON Reports**: Detailed test results saved to timestamped files
- **Console Output**: Real-time test progress and results
- **Performance Metrics**: Response time analysis and statistics

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Make sure you're in the ai_chatbot directory
cd ai_chatbot

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 2. Server Connection Issues
```bash
# Check if server is running
curl http://localhost:8081/health

# Start server if needed
python main.py
```

#### 3. Missing Dependencies
```bash
# Install required packages
pip install pytest requests python-dotenv

# For performance tests
pip install statistics
```

#### 4. Test Failures
```bash
# Run with verbose output
python -m pytest tests/unit/ -v

# Check specific test
python tests/unit/test_handlers.py -v
```

## 🎯 Best Practices

### 1. **Test Isolation**
- Each test should be independent
- Use mock objects for external dependencies
- Clean up test data after each test

### 2. **Naming Conventions**
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### 3. **Test Organization**
- Group related tests in classes
- Use descriptive test names
- Include setup and teardown methods

### 4. **Error Handling**
- Test both success and failure cases
- Validate error messages and status codes
- Test edge cases and boundary conditions

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Chatbot Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest requests
      - name: Run unit tests
        run: python -m pytest tests/unit/
      - name: Run integration tests
        run: |
          python main.py &
          sleep 10
          python tests/integration/test_chat_endpoints.py
```

## 📚 Additional Resources

### Documentation
- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Testing Best Practices](https://realpython.com/python-testing/)

### Testing Patterns
- [Arrange-Act-Assert](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [Behavior-Driven Development](https://en.wikipedia.org/wiki/Behavior-driven_development)

---

**Happy Testing! 🧪✨**
