# app/config.py
import os
from typing import Optional, List
from pydantic import ConfigDict, PostgresDsn, validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application Settings loaded from environment variables"""
    
    # 1. FastAPI Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "SEMS")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", False)

    # 2. Security Settings
    SECRET_KEY: str = os.getenv("SECRETE_KEY", None)
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES', 30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS', 7)

    # 3. CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI itself
    ]


    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 4. Database Settings
    # PostgreSQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USRE", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "root#sgetme")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "exam_api")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    # SQLite (for development)
    SQLITE_DATABASE_URL: Optional[str] = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./data.db")

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get synchronous database URL for Alembic migrations"""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("+asyncpg", "")
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    

    # 5. Redis Cache Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # 6. Email Settings (for notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # 7. Attendance System Specific Settings
    WORKING_HOURS_START: str = "09:00"
    WORKING_HOURS_END: str = "18:00"
    LUNCH_BREAK_START: str = "13:00"
    LUNCH_BREAK_END: str = "14:00"
    TEA_BREAK_DURATION_MINUTES: int = 15
    MINIMUM_WORKING_HOURS: int = 8
    LATE_ARRIVAL_THRESHOLD_MINUTES: int = 15
    EARLY_DEPARTURE_THRESHOLD_MINUTES: int = 30
    
    # 8. File Upload Settings
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf", "csv", "xlsx"]
    UPLOAD_DIR: str = "./uploads"
    
    # 9. Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "./logs/attendance.log"
    
    # 10. Testing Settings
    TESTING: bool = False
    TEST_DATABASE_URL: Optional[str] = "sqlite+aiosqlite:///./test.db"
    
    # Pydantic V2 Config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env
    )
