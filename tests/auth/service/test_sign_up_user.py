from unittest.mock import patch
import pytest
from fastapi import HTTPException
from app.auth import service
from app.users import schemas


# Should return 200 and access token when signing up
@pytest.mark.unit
def test_sign_up_user_should_return_auth_base(mock_db):
    user_data = schemas.UserCreate(
        email="test@example.com", hashed_password="hashed_password"
    )
    db_user = schemas.User(id=1, email="test@example.com", is_active=True)
    tokens = {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }

    with patch(
        "app.users.crud.get_user_by_email", return_value=None
    ) as mock_get_user_by_email, patch(
        "app.users.crud.create_user", return_value=db_user
    ) as mock_create_user, patch(
        "app.core.security.create_tokens", return_value=tokens
    ) as mock_create_token:

        result = service.sign_up_user(user_data, mock_db)

        mock_get_user_by_email.assert_called_once_with(mock_db, email=user_data.email)
        mock_create_user.assert_called_once_with(db=mock_db, user=user_data)
        mock_create_token.assert_called_once_with(db_user.id)

        assert result.tokens.model_dump() == tokens
        assert result.token_type == "bearer"
        assert result.user.id == db_user.id
        assert result.user.email == db_user.email
        assert result.user.is_active == db_user.is_active


# Should return 400 when email already exists
@pytest.mark.unit
def test_sign_up_user_email_already_registered(mock_db):
    user_data = schemas.UserCreate(
        email="test@example.com", hashed_password="hashed_password"
    )
    db_user = schemas.User(id=1, email="test@example.com", is_active=True)

    with patch(
        "app.users.crud.get_user_by_email", return_value=db_user
    ) as mock_get_user_by_email:
        with pytest.raises(HTTPException) as exc_info:
            service.sign_up_user(user_data, mock_db)

        mock_get_user_by_email.assert_called_once_with(mock_db, email=user_data.email)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Email already registered"
