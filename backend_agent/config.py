import os
from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    app_name: str = "Job Platform Backend Agent"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # CORS
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    cors_credentials: bool = Field(default=True, env="CORS_CREDENTIALS")
    
    # Security
    secret_key: str = Field(default="your-secret-key-here", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Database (configure based on your choice)
    database_url: Optional[str] = Field(default=None, env="DATABASE_URL")
    database_name: str = Field(default="job_platform", env="DATABASE_NAME")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    redis_db: int = Field(default=0, env="REDIS_DB")
    
    # Upwork API
    upwork_enabled: bool = Field(default=True, env="UPWORK_ENABLED")
    upwork_api_key: Optional[str] = Field(default=None, env="UPWORK_API_KEY")
    upwork_api_secret: Optional[str] = Field(default=None, env="UPWORK_API_SECRET")
    upwork_access_token: Optional[str] = Field(default=None, env="UPWORK_ACCESS_TOKEN")
    upwork_access_token_secret: Optional[str] = Field(default=None, env="UPWORK_ACCESS_TOKEN_SECRET")
    
    # Fiverr API
    fiverr_enabled: bool = Field(default=True, env="FIVERR_ENABLED")
    fiverr_api_key: Optional[str] = Field(default=None, env="FIVERR_API_KEY")
    fiverr_api_secret: Optional[str] = Field(default=None, env="FIVERR_API_SECRET")
    
    # Fetch.ai
    fetchai_enabled: bool = Field(default=True, env="FETCHAI_ENABLED")
    fetchai_network: str = Field(default="testnet", env="FETCHAI_NETWORK")
    fetchai_entity_file: Optional[str] = Field(default=None, env="FETCHAI_ENTITY_FILE")
    
    # ICP Blockchain
    icp_enabled: bool = Field(default=False, env="ICP_ENABLED")
    icp_network: str = Field(default="mainnet", env="ICP_NETWORK")
    icp_canister_id: Optional[str] = Field(default=None, env="ICP_CANISTER_ID")
    icp_identity_file: Optional[str] = Field(default=None, env="ICP_IDENTITY_FILE")
    
    # Scraping
    scraping_enabled: bool = Field(default=True, env="SCRAPING_ENABLED")
    scraping_workers: int = Field(default=3, env="SCRAPING_WORKERS")
    scraping_rate_limit_per_minute: int = Field(default=60, env="SCRAPING_RATE_LIMIT_PER_MINUTE")
    scraping_rate_limit_per_hour: int = Field(default=1000, env="SCRAPING_RATE_LIMIT_PER_HOUR")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Monitoring
    metrics_enabled: bool = Field(default=True, env="METRICS_ENABLED")
    health_check_interval: int = Field(default=30, env="HEALTH_CHECK_INTERVAL")
    
    # AI/ML
    ai_model_endpoint: Optional[str] = Field(default=None, env="AI_MODEL_ENDPOINT")
    ai_model_api_key: Optional[str] = Field(default=None, env="AI_MODEL_API_KEY")
    
    # External Services
    email_service_url: Optional[str] = Field(default=None, env="EMAIL_SERVICE_URL")
    email_service_api_key: Optional[str] = Field(default=None, env="EMAIL_SERVICE_API_KEY")
    
    # File Storage
    storage_type: str = Field(default="local", env="STORAGE_TYPE")  # local, s3, gcs
    storage_bucket: Optional[str] = Field(default=None, env="STORAGE_BUCKET")
    storage_region: Optional[str] = Field(default=None, env="STORAGE_REGION")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()

def get_config_dict() -> Dict[str, Any]:
    """Get configuration as dictionary"""
    settings = get_settings()
    return {
        "upwork": {
            "enabled": settings.upwork_enabled,
            "api_key": settings.upwork_api_key,
            "api_secret": settings.upwork_api_secret,
            "access_token": settings.upwork_access_token,
            "access_token_secret": settings.upwork_access_token_secret
        },
        "fiverr": {
            "enabled": settings.fiverr_enabled,
            "api_key": settings.fiverr_api_key,
            "api_secret": settings.fiverr_api_secret
        },
        "fetchai": {
            "enabled": settings.fetchai_enabled,
            "network": settings.fetchai_network,
            "entity_file": settings.fetchai_entity_file
        },
        "blockchain": {
            "enabled": settings.icp_enabled,
            "network": settings.icp_network,
            "canister_id": settings.icp_canister_id,
            "identity_file": settings.icp_identity_file
        },
        "scraping": {
            "enabled": settings.scraping_enabled,
            "workers": settings.scraping_workers,
            "rate_limits": {
                "upwork": {
                    "requests_per_minute": settings.scraping_rate_limit_per_minute,
                    "requests_per_hour": settings.scraping_rate_limit_per_hour
                },
                "fiverr": {
                    "requests_per_minute": settings.scraping_rate_limit_per_minute * 2,
                    "requests_per_hour": settings.scraping_rate_limit_per_hour * 2
                }
            }
        },
        "identity": {
            "jwt_secret": settings.secret_key,
            "jwt_expiry_hours": settings.access_token_expire_minutes // 60,
            "max_sessions_per_user": 5
        },
        "database": {
            "url": settings.database_url,
            "name": settings.database_name
        },
        "redis": {
            "url": settings.redis_url,
            "db": settings.redis_db
        },
        "ai": {
            "model_endpoint": settings.ai_model_endpoint,
            "api_key": settings.ai_model_api_key
        }
    }

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Use test networks for development
    fetchai_network: str = "testnet"
    icp_network: str = "testnet"

class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    log_level: str = "WARNING"
    workers: int = 4
    
    # Production should have all required secrets
    secret_key: str = Field(..., env="SECRET_KEY")
    upwork_api_key: str = Field(..., env="UPWORK_API_KEY")
    fiverr_api_key: str = Field(..., env="FIVERR_API_KEY")

class TestSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    database_name: str = "job_platform_test"
    redis_db: int = 1
    
    # Disable external services for testing
    upwork_enabled: bool = False
    fiverr_enabled: bool = False
    icp_enabled: bool = False

def get_environment_settings(environment: str = None) -> Settings:
    """Get environment-specific settings"""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()

# Default configuration
config = get_config_dict() 