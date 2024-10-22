import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, call, ANY
from app.main import app
from app.users import schemas
from app.auth import schemas as authschemas

# Create the test client
client = TestClient(app)


# Should return 200 and access token when signing up
@pytest.mark.unit
def test_sign_up_should_return_200_and_access_token(override_get_db, override_get_current_user, mock_db):
    user_data = {"email": "test@example.com", "hashed_password": "hashed_password"}
    mock_response = authschemas.AuthBase(
        access_token="fake_access_token",
        token_type="bearer",
        user=schemas.UserRepr(id=1, email="test@example.com", is_active=True)
    )

    with patch("app.auth.service.sign_up_user", return_value=mock_response) as mock_sign_up_user:
        response = client.post("/auth/signup", json=user_data)
        assert response.status_code == 200
        assert response.json() == mock_response.model_dump()
        assert mock_sign_up_user.call_args == call(schemas.UserCreate(**user_data), ANY)


# Should return 400 when email already exists
@pytest.mark.unit
def test_sign_up_should_raise_exception(override_get_db, override_get_current_user, mock_db):
    user_data = {"email": "test@example.com", "hashed_password": "hashed_password"}

    # Force sign_up_user to raise an exception
    with patch("app.auth.service.sign_up_user", side_effect=HTTPException(status_code=400, detail="Error creating user")) as mock_sign_up_user:
        response = client.post("/auth/signup", json=user_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Error creating user"}
        assert mock_sign_up_user.call_args == call(schemas.UserCreate(**user_data), ANY)
        