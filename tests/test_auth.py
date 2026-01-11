# tests/test_auth.py
import pytest
from fastapi import status
from app.core.security import create_access_token, verify_token

def test_login_success(client, test_user):
    """Test successful login with form data."""
    response = client.post(
        "/users/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify token is valid
    token_data = verify_token(data["access_token"])
    assert token_data is not None

def test_login_json_success(client, test_user):
    """Test successful login with JSON body."""
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_login_wrong_password(client, test_user):
    """Test login with incorrect password."""
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid username or password" in response.json()["detail"]

def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "password"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_missing_fields(client):
    """Test login with missing required fields."""
    response = client.post(
        "/auth/login",
        data={"username": "testuser"}
        # Missing password
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_token_creation():
    """Test JWT token creation."""
    user_id = "12345"
    token = create_access_token(data={"sub": user_id})
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Verify token can be decoded
    decoded = verify_token(token)
    assert decoded == user_id

def test_token_verification_invalid():
    """Test verification of invalid token."""
    with pytest.raises(Exception):
        verify_token("invalid.token.here")