from unittest.mock import MagicMock, patch
import pytest
from sqlalchemy.orm import Session
from app.users.model import User


@pytest.fixture
def mock_db():
    """Mock the database session dependency."""
    return MagicMock(spec=Session)


@pytest.fixture
def fake_active_user():
    """Create and return a fake active user object."""
    return User(
        id=1, email="test@example.com", hashed_password="hashed_pwd", is_active=True
    )


@pytest.fixture
def fake_inactive_user():
    """Create and return a fake inactive user object."""
    return User(
        id=1, email="test@example.com", hashed_password="hashed_pwd", is_active=True
    )


@pytest.fixture
def override_get_db(mock_db):
    """Override the get_db dependency with a mock database session."""
    with patch("app.core.database.get_db", return_value=mock_db):
        yield


@pytest.fixture
def override_get_current_user(mock_current_user):
    """Override the get_current_user dependency with a mock user object."""
    with patch("app.core.guards.get_current_user", return_value=mock_current_user):
        yield


@pytest.fixture
def mock_current_user():
    """Mock the current user dependency."""
    return User(id=1, email="test@example.com", is_active=True)


@pytest.fixture
def mock_create_access_token():
    """Mock the create_access_token dependency."""
    with patch("app.core.security.create_access_token") as mock_access_token:
        yield mock_access_token


@pytest.fixture
def mock_create_refresh_token():
    """Mock the create_refresh_token dependency."""
    with patch("app.core.security.create_refresh_token") as mock_refresh_token:
        yield mock_refresh_token
