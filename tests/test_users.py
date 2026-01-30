# tests/test_user.py
import pytest
from fastapi import status
from app.core.security import create_access_token, verify_token
from tests.conftest import TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD


def test_create_user_success(client):
    """Test successful user creation."""
    response = client.post(
        "/users/create",
        json={
            "username": TEST_USERNAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == TEST_USERNAME
    assert data["email"] == TEST_EMAIL
    assert "id" in data     
    assert "created_at" in data
    assert "updated_at" in data


def test_create_user_existing_username(client, test_user):
    """Test user creation with existing username."""
    response = client.post(
        "/users/create",
        json={
            "username": TEST_USERNAME,
            "email": "test@example.com",
            "password": TEST_PASSWORD
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST  