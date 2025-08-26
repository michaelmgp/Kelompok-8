"""
Configuration management for the Explorer Agent

Handles environment variables and application settings
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Server Configuration
    port: int = Field(default=8001, env="EXPLORER_AGENT_PORT")
    host: str = Field(default="0.0.0.0", env="EXPLORER_AGENT_HOST")
    debug: bool = Field(default=False, env="EXPLORER_AGENT_DEBUG")
    
    # Scraping Configuration
    rate_limit: int = Field(default=2, env="EXPLORER_AGENT_RATE_LIMIT")
    user_agent: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        env="EXPLORER_AGENT_USER_AGENT"
    )
    max_retries: int = Field(default=3, env="EXPLORER_AGENT_MAX_RETRIES")
    timeout: int = Field(default=30, env="EXPLORER_AGENT_TIMEOUT")
    
    # Job Sources Configuration
    enable_linkedin: bool = Field(default=True, env="EXPLORER_AGENT_ENABLE_LINKEDIN")
    enable_indeed: bool = Field(default=True, env="EXPLORER_AGENT_ENABLE_INDEED")
    enable_glassdoor: bool = Field(default=True, env="EXPLORER_AGENT_ENABLE_GLASSDOOR")
    enable_stackoverflow: bool = Field(default=True, env="EXPLORER_AGENT_ENABLE_STACKOVERFLOW")
    
    # AI Processing Configuration
    ai_enabled: bool = Field(default=True, env="EXPLORER_AGENT_AI_ENABLED")
    ai_model: str = Field(default="gpt-3.5-turbo", env="EXPLORER_AGENT_AI_MODEL")
    ai_api_key: Optional[str] = Field(default=None, env="EXPLORER_AGENT_AI_API_KEY")
    
    # Database Configuration
    redis_url: Optional[str] = Field(default="redis://localhost:6379", env="EXPLORER_AGENT_REDIS_URL")
    db_url: Optional[str] = Field(default="sqlite:///explorer_agent.db", env="EXPLORER_AGENT_DB_URL")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="EXPLORER_AGENT_LOG_LEVEL")
    log_file: str = Field(default="explorer_agent.log", env="EXPLORER_AGENT_LOG_FILE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()

# Global settings instance
settings = get_settings()

