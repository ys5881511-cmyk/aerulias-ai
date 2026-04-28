# Configuration and Constants

import os
from typing import Optional
from enum import Enum
from pydantic import BaseSettings, Field


class Environment(str, Enum):
    """Application environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    # Environment
    ENV: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Application environment"
    )
    DEBUG: bool = Field(
        default=False,
        description="Debug mode enabled"
    )
    
    # API Configuration
    OPENROUTER_API_KEY: str = Field(
        ...,
        description="OpenRouter API key for LLM access"
    )
    OPENROUTER_BASE_URL: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API base URL"
    )
    OPENROUTER_MODEL: str = Field(
        default="openai/gpt-4o-mini",
        description="OpenRouter model identifier"
    )
    OPENROUTER_SITE_URL: str = Field(
        default="http://localhost",
        description="Site URL for API usage tracking"
    )
    OPENROUTER_APP_NAME: str = Field(
        default="aerulias_ai",
        description="Application name for API tracking"
    )
    
    # Model Parameters
    GENERATOR_TEMPERATURE: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Temperature for generator (creativity)"
    )
    EVALUATOR_TEMPERATURE: float = Field(
        default=0.2,
        ge=0.0,
        le=1.0,
        description="Temperature for evaluator (consistency)"
    )
    REFINER_TEMPERATURE: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Temperature for refiner"
    )
    
    # Pipeline Configuration
    EVALUATOR_TARGET_SCORE: int = Field(
        default=80,
        ge=0,
        le=100,
        description="Target evaluation score for refinement loop"
    )
    REFINER_MAX_ITERATIONS: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum refinement iterations"
    )
    REQUEST_TIMEOUT_SECONDS: int = Field(
        default=30,
        ge=5,
        description="API request timeout"
    )
    MAX_RETRIES: int = Field(
        default=3,
        ge=1,
        description="Maximum API retry attempts"
    )
    
    # Memory Configuration
    MEMORY_ENABLED: bool = Field(
        default=True,
        description="Enable local memory store"
    )
    MEMORY_STORE_PATH: str = Field(
        default="memory_store.json",
        description="Path to memory store file"
    )
    MEMORY_MAX_SIZE: int = Field(
        default=1000,
        description="Maximum memory entries"
    )
    
    # Logging Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    LOG_FORMAT: str = Field(
        default="json",
        description="Log format (json or text)"
    )
    
    # Server Configuration
    API_HOST: str = Field(
        default="0.0.0.0",
        description="API server host"
    )
    API_PORT: int = Field(
        default=8000,
        description="API server port"
    )
    WORKERS: int = Field(
        default=4,
        description="Number of worker processes"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Requests per minute per client"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings: Settings = Settings()


# Constants
class Constants:
    """Application constants."""
    
    # Scoring thresholds
    SCORE_EXCELLENT = 90
    SCORE_GOOD = 75
    SCORE_ACCEPTABLE = 60
    SCORE_POOR = 40
    
    # Timeout values (seconds)
    API_TIMEOUT = settings.REQUEST_TIMEOUT_SECONDS
    EVALUATION_TIMEOUT = 45
    REFINEMENT_TIMEOUT = 60
    
    # Cache settings
    CACHE_TTL_SECONDS = 3600  # 1 hour
    MAX_CACHE_SIZE_MB = 100
    
    # Prompt constraints
    MAX_QUERY_LENGTH = 2000
    MAX_ANSWER_LENGTH = 8000
    MIN_QUERY_LENGTH = 5
    MIN_ANSWER_LENGTH = 10
    
    # API constraints
    MAX_BATCH_SIZE = 10
    MAX_PARALLEL_REQUESTS = 5
    
    # Retry strategy
    RETRY_INITIAL_DELAY = 1  # seconds
    RETRY_MAX_DELAY = 30
    RETRY_MULTIPLIER = 2.0
    
    # Error messages
    INVALID_QUERY_MESSAGE = "Query must be between 5-2000 characters"
    INVALID_ANSWER_MESSAGE = "Answer must be between 10-8000 characters"
    API_ERROR_MESSAGE = "API service temporarily unavailable"
    TIMEOUT_ERROR_MESSAGE = "Request timeout"
    RATE_LIMIT_ERROR_MESSAGE = "Rate limit exceeded"
    
    # Response status codes
    STATUS_SUCCESS = 200
    STATUS_BAD_REQUEST = 400
    STATUS_UNAUTHORIZED = 401
    STATUS_RATE_LIMITED = 429
    STATUS_SERVER_ERROR = 500


def get_settings() -> Settings:
    """Get application settings."""
    return settings


def validate_configuration() -> bool:
    """Validate critical configuration."""
    if not settings.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is required")
    
    if not (0 <= settings.GENERATOR_TEMPERATURE <= 1.0):
        raise ValueError("GENERATOR_TEMPERATURE must be between 0 and 1")
    
    if not (0 <= settings.EVALUATOR_TEMPERATURE <= 1.0):
        raise ValueError("EVALUATOR_TEMPERATURE must be between 0 and 1")
    
    if not (0 <= settings.EVALUATOR_TARGET_SCORE <= 100):
        raise ValueError("EVALUATOR_TARGET_SCORE must be between 0 and 100")
    
    return True
