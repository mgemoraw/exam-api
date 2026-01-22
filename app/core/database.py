from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os 

# user environment variables in production
DATABASE_URL  = os.getenv('SQLITE_DB_URL', 'sqlite:///./data.db')

engine= create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    echo=True,
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