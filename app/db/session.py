# db/session.py
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.core.config import settings  # Your DB URL from pydantic settings
import os

DATABASE_URL  = os.getenv('SQLITE_DB_URL', 'sqlite:///./data.db')
# Create Async Engine
async_engine: AsyncEngine = create_async_engine(
    settings.ASYNC_DATABASE_URL,  # e.g., postgresql+asyncpg://user:pass@localhost/db
    echo=False,                   # Set True for SQL logs
    future=True,
)

# Create Sync Engine
engine = create_engine(
    # settings.DATABASE_URL,
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    echo=False,
    connect_args={"check_same_thread": False}  # Only for SQLite
)

# Async session factory
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Keep objects usable after commit
)

# Sync session factory
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

