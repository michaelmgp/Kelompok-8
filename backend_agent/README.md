# Job Platform Backend Agent

A comprehensive, AI-powered backend system for job aggregation and analysis across multiple freelance platforms (Upwork, Fiverr) with Fetch.ai agent integration and ICP blockchain support.

## 🏗️ Architecture Overview

```
backend_agent/
├── agents/                    # Fetch.ai agents for platform integration
│   ├── upwork_agent.py       # Upwork job scraping and analysis
│   ├── fiverr_agent.py       # Fiverr gig discovery and analysis
│   └── coordinator.py        # Multi-platform coordination and aggregation
├── api/                      # FastAPI REST API layer
│   ├── routes.py             # Main API endpoints and business logic
│   └── icp_integration.py    # ICP blockchain integration
├── services/                 # Core business logic services
│   ├── scraper.py            # Job scraping orchestration
│   ├── job_formatter.py      # Data formatting and analytics
│   └── identity_manager.py   # User profile and authentication
├── tests/                    # Test suite
├── main.py                   # FastAPI application entry point
├── config.py                 # Configuration management
└── requirements.txt          # Python dependencies
```

## 🚀 Features

### Core Functionality

- **Multi-Platform Job Aggregation**: Unified search across Upwork and Fiverr
- **AI-Powered Job Scoring**: Intelligent job matching and relevance scoring
- **Real-time Scraping**: Automated job discovery with rate limiting
- **User Management**: Complete user authentication and profile system
- **Proposal Management**: Submit proposals directly from the platform

### Advanced Features

- **Fetch.ai Integration**: Decentralized agent coordination
- **ICP Blockchain**: Job verification and smart contract integration
- **Analytics Engine**: Comprehensive job market insights
- **Personalization**: AI-driven job recommendations
- **Export Capabilities**: Multiple data export formats (JSON, CSV)

### Technical Features

- **Async Architecture**: High-performance asynchronous processing
- **Rate Limiting**: Platform-specific API rate limit management
- **Health Monitoring**: Comprehensive system health checks
- **Scalable Design**: Worker-based scraping architecture
- **RESTful API**: Clean, documented API endpoints
- **Schema Compliance**: Strict JSON schema validation

## 📚 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Standardized Job Search API

The API now implements a standardized JSON schema for job search requests and responses, ensuring consistency across all platforms.

#### Job Search Request

**Endpoint**: `POST /api/v1/jobs/search`

**Request Schema**:

```json
{
  "skills": ["java", "backend"],
  "keywords": ["spring boot", "api"],
  "budget_min": 800,
  "budget_max": 2000,
  "rate_type": "fixed",
  "remote": true,
  "duration_days_max": 30,
  "top_k": 10,
  "location": "Remote-Only",
  "currency": "USD",
  "sources": ["upwork", "fiverr", "linkedin", "glints"],
  "sort_by": "relevance",
  "cursor": null,
  "page_size": 20
}
```

**Field Descriptions**:

- `skills`: Array of required skills (default: `[]`)
- `keywords`: Array of search keywords (default: `[]`)
- `budget_min`: Minimum budget amount (optional)
- `budget_max`: Maximum budget amount (optional)
- `rate_type`: Rate type - `"fixed"`, `"hourly"`, or `null` (optional)
- `remote`: Remote work preference (optional)
- `duration_days_max`: Maximum project duration in days (optional)
- `top_k`: Top K results (1-50, default: 5)
- `location`: Location preference (e.g., 'Jakarta', 'Remote-Only')
- `currency`: ISO 4217 currency code (e.g., 'USD', 'IDR')
- `sources`: Platform sources to search (default: `["upwork", "fiverr"]`)
- `sort_by`: Sorting criteria - `"relevance"`, `"recent"`, `"budget_desc"`, `"budget_asc"` (default: `"relevance"`)
- `cursor`: Pagination cursor (optional)
- `page_size`: Results per page (1-50, default: 20)

#### Job Search Response

**Response Schema**:

```json
{
  "jobs": [
    {
      "id": "upwork:1234567890",
      "source": "upwork",
      "source_id": "1234567890",
      "title": "Java Backend API for Fintech",
      "company": "FinCo Labs",
      "url": "https://www.upwork.com/jobs/1234567890",
      "description": "Build REST APIs in Spring Boot...",
      "skills": ["java", "spring boot", "rest", "postgresql"],
      "keywords": ["backend", "api", "microservices"],
      "rate_type": "fixed",
      "budget_min": 1000.0,
      "budget_max": 1500.0,
      "currency": "USD",
      "remote": true,
      "location": null,
      "duration_days_est": 21,
      "posted_at": "2025-08-17T07:13:00Z",
      "updated_at": "2025-08-19T10:02:00Z",
      "source_rating": 4.8,
      "provenance": {
        "fetched_at": "2025-08-21T04:00:00Z",
        "source_url": "https://www.upwork.com/jobs/1234567890",
        "raw_excerpt": "We are hiring a Java backend engineer..."
      },
      "score": 0.91
    }
  ],
  "next_cursor": "eyJwYWdlIjoyfQ==",
  "meta": {
    "request_id": "req-7fdc3a",
    "sources_hit": ["upwork", "linkedin"],
    "took_ms": 980,
    "limits": {
      "rate_limited_sources": ["glints"]
    }
  }
}
```

**Job Object Fields**:

- `id`: Global stable ID in format `<source>:<source_id>`
- `source`: Platform source (`"upwork"`, `"fiverr"`, `"linkedin"`, `"glints"`, `"other"`)
- `source_id`: Original source ID
- `title`: Job title
- `company`: Company name (optional)
- `url`: Job URL
- `description`: Job description (optional)
- `skills`: Required skills array (default: `[]`)
- `keywords`: Job keywords array (default: `[]`)
- `rate_type`: Rate type - `"fixed"`, `"hourly"`, or `null`
- `budget_min`: Minimum budget (optional)
- `budget_max`: Maximum budget (optional)
- `currency`: Currency code (optional)
- `remote`: Remote work option (optional)
- `location`: Job location (optional)
- `duration_days_est`: Estimated duration in days (optional)
- `posted_at`: Posted timestamp in ISO 8601 format (optional)
- `updated_at`: Updated timestamp in ISO 8601 format (optional)
- `source_rating`: Seller/client rating if available (optional)
- `provenance`: Job provenance information
- `score`: Relevance score 0-1 (optional)

**Response Metadata**:

- `request_id`: Unique request identifier
- `sources_hit`: Array of sources that returned results
- `took_ms`: Search execution time in milliseconds
- `limits`: Rate limiting information
- `next_cursor`: Pagination cursor for next page (optional)

### Legacy API Endpoints

For backward compatibility, the following legacy endpoints are still available:

- `POST /api/v1/jobs/search/legacy` - Legacy job search
- `GET /api/v1/jobs/{job_id}` - Get job details (now returns normalized format)
- `GET /api/v1/jobs/trending` - Get trending jobs (now returns normalized format)

### User Management Endpoints

- `GET /api/v1/profile` - Get user profile
- `PUT /api/v1/profile` - Update user profile
- `POST /api/v1/proposals` - Submit job proposal

### Platform Management

- `GET /api/v1/platforms/status` - Platform status
- `GET /api/v1/platforms/categories` - Platform categories

### Analytics & Health

- `GET /api/v1/analytics/job-trends` - Job trends analytics
- `GET /health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health check

## 🔧 Configuration

### Environment Variables

| Variable           | Description                               | Default                         |
| ------------------ | ----------------------------------------- | ------------------------------- |
| `ENVIRONMENT`      | Environment (development/production/test) | `development`                   |
| `DEBUG`            | Enable debug mode                         | `false`                         |
| `SECRET_KEY`       | JWT secret key                            | Required in production          |
| `UPWORK_API_KEY`   | Upwork API key                            | Required for Upwork integration |
| `FIVERR_API_KEY`   | Fiverr API key                            | Required for Fiverr integration |
| `REDIS_URL`        | Redis connection URL                      | `redis://localhost:6379`        |
| `SCRAPING_WORKERS` | Number of scraping workers                | `3`                             |

### Platform Configuration

Each platform can be enabled/disabled independently:

```python
# config.py
config = {
    "upwork": {
        "enabled": True,
        "api_key": "your_key",
        "rate_limits": {"requests_per_minute": 60}
    },
    "fiverr": {
        "enabled": True,
        "api_key": "your_key",
        "rate_limits": {"requests_per_minute": 120}
    }
}
```

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-mock

# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_schema_compliance.py
```

### Test Structure

- **Unit Tests**: Individual component testing
- **Integration Tests**: Service interaction testing
- **Schema Compliance Tests**: JSON schema validation testing
- **Mock Testing**: External API mocking for reliable testing

## 📊 Monitoring & Health Checks

### Health Endpoints

- `GET /health` - Basic health check
- `GET /api/v1/health/detailed` - Comprehensive system status
- `GET /api/v1/platforms/status` - Platform-specific status

### Metrics

- Job scraping statistics
- API response times
- Platform availability
- User session metrics

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set all required secrets
2. **Database**: Configure production database
3. **Redis**: Production Redis instance
4. **Rate Limiting**: Adjust platform-specific limits
5. **Monitoring**: Enable comprehensive logging
6. **Security**: HTTPS, CORS configuration

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: job-platform-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: job-platform-backend
  template:
    metadata:
      labels:
        app: job-platform-backend
    spec:
      containers:
        - name: backend
          image: job-platform-backend:latest
          ports:
            - containerPort: 8000
          env:
            - name: ENVIRONMENT
              value: "production"
```

## 🔒 Security

### Authentication

- JWT-based authentication
- Session management
- Password hashing (SHA-256)

### API Security

- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention

### Data Protection

- Sensitive data encryption
- Secure API key storage
- Audit logging

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints
- Include docstrings
- Write comprehensive tests
- Ensure JSON schema compliance

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

1. **Redis Connection**: Ensure Redis is running and accessible
2. **API Keys**: Verify platform API keys are valid
3. **Rate Limits**: Check platform-specific rate limiting
4. **Dependencies**: Ensure all Python packages are installed
5. **Schema Validation**: Verify request/response format compliance

### Getting Help

- Check the API documentation at `/docs`
- Review the logs for error details
- Check the health endpoints for system status
- Open an issue on GitHub

## 🔮 Roadmap

### Planned Features

- [ ] Additional platform support (Freelancer, Guru)
- [ ] Advanced AI job matching
- [ ] Real-time notifications
- [ ] Mobile app support
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Advanced blockchain features

### Performance Improvements

- [ ] Database optimization
- [ ] Caching strategies
- [ ] Load balancing
- [ ] Microservices architecture

---

**Note**: This implementation enforces strict JSON schema compliance for all API requests and responses. The standardized format ensures consistency across platforms and provides a robust foundation for job aggregation and analysis.
