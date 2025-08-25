import pytest
import json
from datetime import datetime
from typing import Dict, Any

from api.routes import SearchRequest, Job, JobProvenance, SearchResponse, SearchResponseMeta

class TestSchemaCompliance:
    """Test cases to verify JSON schema compliance"""
    
    def test_search_request_schema(self):
        """Test SearchRequest model validation"""
        # Valid request
        valid_request = {
            "skills": ["java", "backend"],
            "keywords": ["spring boot", "api"],
            "budget_min": 800,
            "rate_type": "fixed",
            "remote": True,
            "duration_days_max": 30,
            "currency": "USD",
            "sources": ["linkedin", "glints", "fiverr", "upwork"],
            "sort_by": "relevance",
            "page_size": 10
        }
        
        request = SearchRequest(**valid_request)
        assert request.skills == ["java", "backend"]
        assert request.keywords == ["spring boot", "api"]
        assert request.budget_min == 800
        assert request.rate_type == "fixed"
        assert request.remote is True
        assert request.duration_days_max == 30
        assert request.currency == "USD"
        assert request.sources == ["linkedin", "glints", "fiverr", "upwork"]
        assert request.sort_by == "relevance"
        assert request.page_size == 10
        
        # Test defaults
        minimal_request = {}
        request = SearchRequest(**minimal_request)
        assert request.skills == []
        assert request.keywords == []
        assert request.top_k == 5
        assert request.page_size == 20
        assert request.sort_by == "relevance"
        assert request.sources == ["upwork", "fiverr"]
    
    def test_search_request_validation(self):
        """Test SearchRequest validation rules"""
        # Test budget validation
        with pytest.raises(ValueError, match="budget_max must be greater than or equal to budget_min"):
            SearchRequest(budget_min=1000, budget_max=500)
        
        # Test valid budget range
        request = SearchRequest(budget_min=500, budget_max=1000)
        assert request.budget_min == 500
        assert request.budget_max == 1000
        
        # Test enum validation
        with pytest.raises(ValueError):
            SearchRequest(rate_type="invalid")
        
        with pytest.raises(ValueError):
            SearchRequest(sort_by="invalid")
        
        with pytest.raises(ValueError):
            SearchRequest(sources=["invalid_platform"])
    
    def test_job_schema(self):
        """Test Job model validation"""
        # Valid job
        valid_job = {
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
            "remote": True,
            "location": None,
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
        
        job = Job(**valid_job)
        assert job.id == "upwork:1234567890"
        assert job.source == "upwork"
        assert job.source_id == "1234567890"
        assert job.title == "Java Backend API for Fintech"
        assert job.company == "FinCo Labs"
        assert job.url == "https://www.upwork.com/jobs/1234567890"
        assert job.description == "Build REST APIs in Spring Boot..."
        assert job.skills == ["java", "spring boot", "rest", "postgresql"]
        assert job.keywords == ["backend", "api", "microservices"]
        assert job.rate_type == "fixed"
        assert job.budget_min == 1000.0
        assert job.budget_max == 1500.0
        assert job.currency == "USD"
        assert job.remote is True
        assert job.location is None
        assert job.duration_days_est == 21
        assert job.posted_at == "2025-08-17T07:13:00Z"
        assert job.updated_at == "2025-08-19T10:02:00Z"
        assert job.source_rating == 4.8
        assert job.score == 0.91
        
        # Test provenance
        assert job.provenance is not None
        assert job.provenance.fetched_at == "2025-08-21T04:00:00Z"
        assert job.provenance.source_url == "https://www.upwork.com/jobs/1234567890"
        assert job.provenance.raw_excerpt == "We are hiring a Java backend engineer..."
    
    def test_job_validation(self):
        """Test Job model validation rules"""
        # Test required fields
        with pytest.raises(ValueError):
            Job()  # Missing required fields
        
        # Test enum validation
        with pytest.raises(ValueError):
            Job(
                id="test:123",
                source="invalid_source",
                source_id="123",
                title="Test Job",
                url="https://example.com"
            )
        
        with pytest.raises(ValueError):
            Job(
                id="test:123",
                source="upwork",
                source_id="123",
                title="Test Job",
                url="https://example.com",
                rate_type="invalid_rate_type"
            )
        
        # Test score range validation
        with pytest.raises(ValueError):
            Job(
                id="test:123",
                source="upwork",
                source_id="123",
                title="Test Job",
                url="https://example.com",
                score=1.5  # Should be <= 1.0
            )
        
        with pytest.raises(ValueError):
            Job(
                id="test:123",
                source="upwork",
                source_id="123",
                title="Test Job",
                url="https://example.com",
                score=-0.1  # Should be >= 0.0
            )
    
    def test_search_response_schema(self):
        """Test SearchResponse model validation"""
        # Valid response
        valid_response = {
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
                    "remote": True,
                    "location": None,
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
                "sources_hit": ["upwork"],
                "took_ms": 980,
                "limits": {"rate_limited_sources": ["glints"]}
            }
        }
        
        response = SearchResponse(**valid_response)
        assert len(response.jobs) == 1
        assert response.jobs[0].id == "upwork:1234567890"
        assert response.next_cursor == "eyJwYWdlIjoyfQ=="
        assert response.meta.request_id == "req-7fdc3a"
        assert response.meta.sources_hit == ["upwork"]
        assert response.meta.took_ms == 980
        assert response.meta.limits["rate_limited_sources"] == ["glints"]
    
    def test_json_serialization(self):
        """Test that models can be serialized to JSON"""
        # Create a complete search request
        request = SearchRequest(
            skills=["java", "backend"],
            keywords=["spring boot", "api"],
            budget_min=800,
            rate_type="fixed",
            remote=True,
            duration_days_max=30,
            currency="USD",
            sources=["upwork", "fiverr"],
            sort_by="relevance",
            page_size=10
        )
        
        # Serialize to JSON
        json_str = request.json()
        assert isinstance(json_str, str)
        
        # Deserialize and verify
        parsed = json.loads(json_str)
        assert parsed["skills"] == ["java", "backend"]
        assert parsed["keywords"] == ["spring boot", "api"]
        assert parsed["budget_min"] == 800
        assert parsed["rate_type"] == "fixed"
        assert parsed["remote"] is True
        assert parsed["duration_days_max"] == 30
        assert parsed["currency"] == "USD"
        assert parsed["sources"] == ["upwork", "fiverr"]
        assert parsed["sort_by"] == "relevance"
        assert parsed["page_size"] == 10
    
    def test_example_request_response(self):
        """Test the exact example from the specification"""
        # Example request
        example_request = {
            "skills": ["java", "backend"],
            "keywords": ["spring boot", "api"],
            "budget_min": 800,
            "rate_type": "fixed",
            "remote": True,
            "duration_days_max": 30,
            "currency": "USD",
            "sources": ["linkedin", "glints", "fiverr", "upwork"],
            "sort_by": "relevance",
            "page_size": 10
        }
        
        request = SearchRequest(**example_request)
        assert request.skills == ["java", "backend"]
        assert request.keywords == ["spring boot", "api"]
        assert request.budget_min == 800
        assert request.rate_type == "fixed"
        assert request.remote is True
        assert request.duration_days_max == 30
        assert request.currency == "USD"
        assert request.sources == ["linkedin", "glints", "fiverr", "upwork"]
        assert request.sort_by == "relevance"
        assert request.page_size == 10
        
        # Example response
        example_response = {
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
                    "remote": True,
                    "location": None,
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
                "limits": {"rate_limited_sources": ["glints"]}
            }
        }
        
        response = SearchResponse(**example_response)
        assert len(response.jobs) == 1
        assert response.jobs[0].id == "upwork:1234567890"
        assert response.jobs[0].source == "upwork"
        assert response.jobs[0].source_id == "1234567890"
        assert response.jobs[0].title == "Java Backend API for Fintech"
        assert response.jobs[0].company == "FinCo Labs"
        assert response.jobs[0].url == "https://www.upwork.com/jobs/1234567890"
        assert response.jobs[0].description == "Build REST APIs in Spring Boot..."
        assert response.jobs[0].skills == ["java", "spring boot", "rest", "postgresql"]
        assert response.jobs[0].keywords == ["backend", "api", "microservices"]
        assert response.jobs[0].rate_type == "fixed"
        assert response.jobs[0].budget_min == 1000.0
        assert response.jobs[0].budget_max == 1500.0
        assert response.jobs[0].currency == "USD"
        assert response.jobs[0].remote is True
        assert response.jobs[0].location is None
        assert response.jobs[0].duration_days_est == 21
        assert response.jobs[0].posted_at == "2025-08-17T07:13:00Z"
        assert response.jobs[0].updated_at == "2025-08-19T10:02:00Z"
        assert response.jobs[0].source_rating == 4.8
        assert response.jobs[0].score == 0.91
        
        # Verify provenance
        assert response.jobs[0].provenance is not None
        assert response.jobs[0].provenance.fetched_at == "2025-08-21T04:00:00Z"
        assert response.jobs[0].provenance.source_url == "https://www.upwork.com/jobs/1234567890"
        assert response.jobs[0].provenance.raw_excerpt == "We are hiring a Java backend engineer..."
        
        # Verify metadata
        assert response.meta.request_id == "req-7fdc3a"
        assert response.meta.sources_hit == ["upwork", "linkedin"]
        assert response.meta.took_ms == 980
        assert response.meta.limits["rate_limited_sources"] == ["glints"]
        
        # Verify pagination
        assert response.next_cursor == "eyJwYWdlIjoyfQ==" 