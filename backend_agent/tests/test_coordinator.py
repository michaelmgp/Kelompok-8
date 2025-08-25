import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from datetime import datetime

from agents.coordinator import Coordinator, UnifiedJob

@pytest.fixture
def mock_config():
    return {
        "upwork": {
            "enabled": True,
            "api_key": "test_upwork_key"
        },
        "fiverr": {
            "enabled": True,
            "api_key": "test_fiverr_key"
        },
        "blockchain": {
            "enabled": False
        }
    }

@pytest.fixture
def mock_coordinator(mock_config):
    return Coordinator(mock_config)

@pytest.fixture
def sample_jobs():
    return [
        UnifiedJob(
            id="upwork_123",
            platform="upwork",
            title="Python Developer Needed",
            description="Looking for experienced Python developer",
            budget="$1000",
            skills=["python", "django", "postgresql"],
            category="development",
            posted_date=datetime.utcnow(),
            url="https://upwork.com/jobs/123",
            ai_score=0.8,
            platform_specific_data={"client_info": {"total_spent": "5000"}}
        ),
        UnifiedJob(
            id="fiverr_456",
            platform="fiverr",
            title="Logo Design",
            description="Professional logo design needed",
            budget="$200",
            skills=["logo design", "illustrator"],
            category="design",
            posted_date=datetime.utcnow(),
            url="https://fiverr.com/gigs/456",
            ai_score=0.7,
            platform_specific_data={"seller_info": {"rating": 4.9}}
        )
    ]

class TestCoordinator:
    """Test cases for Coordinator class"""
    
    @pytest.mark.asyncio
    async def test_initialization(self, mock_coordinator):
        """Test coordinator initialization"""
        assert mock_coordinator.config is not None
        assert mock_coordinator.upwork_agent is None
        assert mock_coordinator.fiverr_agent is None
        assert not mock_coordinator.is_initialized
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, mock_coordinator):
        """Test successful initialization"""
        await mock_coordinator.initialize()
        assert mock_coordinator.is_initialized
        assert mock_coordinator.entity is not None
    
    @pytest.mark.asyncio
    async def test_search_all_platforms_not_initialized(self, mock_coordinator):
        """Test search fails when not initialized"""
        with pytest.raises(RuntimeError, match="Coordinator not initialized"):
            await mock_coordinator.search_all_platforms("python developer")
    
    @pytest.mark.asyncio
    async def test_search_all_platforms_success(self, mock_coordinator, sample_jobs):
        """Test successful search across platforms"""
        # Mock the agents
        mock_coordinator.upwork_agent = Mock()
        mock_coordinator.upwork_agent.search_jobs = AsyncMock(return_value=[sample_jobs[0]])
        
        mock_coordinator.fiverr_agent = Mock()
        mock_coordinator.fiverr_agent.search_gigs = AsyncMock(return_value=[sample_jobs[1]])
        
        mock_coordinator.is_initialized = True
        
        results = await mock_coordinator.search_all_platforms("developer")
        
        assert len(results) == 2
        assert results[0].ai_score >= results[1].ai_score  # Should be sorted by AI score
    
    @pytest.mark.asyncio
    async def test_get_job_details_upwork(self, mock_coordinator, sample_jobs):
        """Test getting Upwork job details"""
        mock_coordinator.upwork_agent = Mock()
        mock_coordinator.upwork_agent.get_job_details = AsyncMock(return_value=sample_jobs[0])
        mock_coordinator.is_initialized = True
        
        result = await mock_coordinator.get_job_details("upwork_123")
        
        assert result is not None
        assert result.platform == "upwork"
        assert result.id == "upwork_123"
    
    @pytest.mark.asyncio
    async def test_get_job_details_fiverr(self, mock_coordinator, sample_jobs):
        """Test getting Fiverr job details"""
        mock_coordinator.fiverr_agent = Mock()
        mock_coordinator.fiverr_agent.get_gig_details = AsyncMock(return_value=sample_jobs[1])
        mock_coordinator.is_initialized = True
        
        result = await mock_coordinator.get_job_details("fiverr_456")
        
        assert result is not None
        assert result.platform == "fiverr"
        assert result.id == "fiverr_456"
    
    @pytest.mark.asyncio
    async def test_get_job_details_invalid_id(self, mock_coordinator):
        """Test getting job details with invalid ID"""
        mock_coordinator.is_initialized = True
        
        result = await mock_coordinator.get_job_details("invalid_789")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_submit_proposal_upwork(self, mock_coordinator):
        """Test submitting proposal to Upwork"""
        mock_coordinator.upwork_agent = Mock()
        mock_coordinator.upwork_agent.submit_proposal = AsyncMock(return_value=True)
        mock_coordinator.is_initialized = True
        
        proposal_data = {
            "cover_letter": "I'm interested in this project",
            "proposed_budget": "$1200",
            "delivery_time": "2 weeks"
        }
        
        result = await mock_coordinator.submit_proposal("upwork_123", proposal_data)
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_submit_proposal_fiverr(self, mock_coordinator):
        """Test submitting proposal to Fiverr (should fail)"""
        mock_coordinator.is_initialized = True
        
        proposal_data = {
            "cover_letter": "I'm interested in this project"
        }
        
        result = await mock_coordinator.submit_proposal("fiverr_456", proposal_data)
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_trending_jobs(self, mock_coordinator, sample_jobs):
        """Test getting trending jobs"""
        mock_coordinator.fiverr_agent = Mock()
        mock_coordinator.fiverr_agent.get_trending_gigs = AsyncMock(return_value=[sample_jobs[1]])
        mock_coordinator.is_initialized = True
        
        results = await mock_coordinator.get_trending_jobs()
        
        assert len(results) == 1
        assert results[0].platform == "fiverr"
    
    @pytest.mark.asyncio
    async def test_get_status(self, mock_coordinator):
        """Test getting coordinator status"""
        status = mock_coordinator.get_status()
        
        assert "initialized" in status
        assert "upwork_enabled" in status
        assert "fiverr_enabled" in status
        assert "blockchain_enabled" in status
    
    @pytest.mark.asyncio
    async def test_cleanup(self, mock_coordinator):
        """Test coordinator cleanup"""
        # Mock agents
        mock_coordinator.upwork_agent = Mock()
        mock_coordinator.upwork_agent.__aexit__ = AsyncMock()
        
        mock_coordinator.fiverr_agent = Mock()
        mock_coordinator.fiverr_agent.__aexit__ = AsyncMock()
        
        await mock_coordinator.cleanup()
        
        # Verify cleanup was called
        mock_coordinator.upwork_agent.__aexit__.assert_called_once()
        mock_coordinator.fiverr_agent.__aexit__.assert_called_once()

class TestUnifiedJob:
    """Test cases for UnifiedJob dataclass"""
    
    def test_unified_job_creation(self):
        """Test UnifiedJob creation with default values"""
        job = UnifiedJob(
            id="test_123",
            platform="upwork",
            title="Test Job",
            description="Test description",
            budget="$100",
            skills=["python"],
            category="development",
            posted_date=datetime.utcnow(),
            url="https://example.com",
            ai_score=0.8,
            platform_specific_data={}
        )
        
        assert job.id == "test_123"
        assert job.platform == "upwork"
        assert job.created_at is not None
    
    def test_unified_job_with_custom_created_at(self):
        """Test UnifiedJob creation with custom created_at"""
        custom_time = datetime(2023, 1, 1, 12, 0, 0)
        
        job = UnifiedJob(
            id="test_456",
            platform="fiverr",
            title="Test Job",
            description="Test description",
            budget="$200",
            skills=["design"],
            category="design",
            posted_date=datetime.utcnow(),
            url="https://example.com",
            ai_score=0.9,
            platform_specific_data={},
            created_at=custom_time
        )
        
        assert job.created_at == custom_time 