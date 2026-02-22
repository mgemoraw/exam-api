from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session, declarative_base, DeclarativeBase
from typing import Generator
import os 

# ASYNC SQLALCHEMY IMPORTS
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker



# user environment variables in production
DATABASE_URL  = os.getenv('SQLITE_DB_URL', 'sqlite:///./data.db')

engine= create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    echo=False,
    connect_args={"check_same_thread": False}  # Only for SQLite
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False, 
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



## ASYNC SQLALCHEMY SETUP
PG_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/exam_db"

async_engine = create_async_engine(PG_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

# Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session



convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    metadata = metadata
    pass
