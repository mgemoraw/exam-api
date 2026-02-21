# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app 
from app.main import app
from app.infrastructure.database import get_db
from app.models.base import Base
from app.models.user import User
from app.core.security import create_access_token, hash_password

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./_test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_USERNAME = "testuser"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "TestPassword#123"



@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user."""
    model = User(
        username=TEST_USERNAME,
        email=TEST_EMAIL,
        hashed_password=hash_password(TEST_PASSWORD),
        is_active=True
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


@pytest.fixture(scope="function")
def test_user_token(test_user):
    """Create access token for test user."""
    return create_access_token(data={"sub": str(test_user.id)})

@pytest.fixture(scope="function")
def authorized_client(client, test_user_token):
    """Create an authorized test client."""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_user_token}"
    }
    return client