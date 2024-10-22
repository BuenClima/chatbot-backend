from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.core.security import create_access_token

# Create the test client
client = TestClient(app)


@pytest.mark.unit
def test_read_current_user_success(mock_current_user):
    access_token = create_access_token(data={"sub": str(mock_current_user.id)})

    # Add the token to the request headers
    headers = {"Authorization": f"Bearer {access_token}"}
    with patch(
        "app.core.guards.get_current_user", return_value=mock_current_user
    ), patch("app.users.crud.get_user_by_id", return_value=mock_current_user):
        response = client.get("/users", headers=headers)
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["id"] == 1
        assert user_data["email"] == "test@example.com"
        assert user_data["is_active"] is True


@pytest.mark.unit
def test_read_current_user_unauthorized():
    with patch(
        "app.core.guards.get_current_user",
        side_effect=HTTPException(status_code=401, detail="Not authenticated"),
    ):
        response = client.get("/users")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}
