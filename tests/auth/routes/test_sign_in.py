import pytest
from unittest.mock import patch
from fastapi import HTTPException
from app.auth import service
from app.auth import schemas as authschemas
from app.users import schemas as userschemas


# Should return 200 and access token when signing in
@pytest.mark.unit
def test_sign_in_user_should_return_200_and_access_token(mock_db):
    form_data = authschemas.AuthSignIn(
        email="test@example.com", hashed_password="hashed_password"
    )
    db_user = userschemas.User(
        id=1,
        email="test@example.com",
        is_active=True,
        hashed_password="hashed_password",
    )

    tokens = {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }

    with patch(
        "app.users.crud.get_user_by_email", return_value=db_user
    ) as mock_get_user_by_email, patch(
        "app.core.security.verify_password", return_value=True
    ) as mock_verify_password, patch(
        "app.core.security.create_tokens", return_value=tokens
    ) as mock_create_tokens:

        result = service.sign_in_user(form_data, mock_db)

        mock_get_user_by_email.assert_called_once_with(mock_db, email=form_data.email)
        mock_verify_password.assert_called_once_with(
            form_data.hashed_password, db_user.hashed_password
        )
        mock_create_tokens.assert_called_once_with(db_user.id)

        assert result.tokens.model_dump() == tokens
        assert result.token_type == "bearer"
        assert result.user.id == db_user.id
        assert result.user.email == db_user.email
        assert result.user.is_active == db_user.is_active


# Should return 400 when email does not exist
@pytest.mark.unit
def test_sign_in_user_incorrect_email(mock_db):
    form_data = authschemas.AuthSignIn(
        email="test@example.com", hashed_password="hashed_password"
    )

    with patch(
        "app.users.crud.get_user_by_email", return_value=None
    ) as mock_get_user_by_email:
        with pytest.raises(HTTPException) as exc_info:
            service.sign_in_user(form_data, mock_db)

        mock_get_user_by_email.assert_called_once_with(mock_db, email=form_data.email)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Email not registered, sign up first"


# Should return 400 when password is incorrect
@pytest.mark.unit
def test_sign_in_user_incorrect_password(mock_db):
    form_data = authschemas.AuthSignIn(
        email="test@example.com", hashed_password="hashed_password"
    )
    db_user = userschemas.User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )

    with patch(
        "app.users.crud.get_user_by_email", return_value=db_user
    ) as mock_get_user_by_email, patch(
        "app.core.security.verify_password", return_value=False
    ) as mock_verify_password:

        with pytest.raises(HTTPException) as exc_info:
            service.sign_in_user(form_data, mock_db)

        mock_get_user_by_email.assert_called_once_with(mock_db, email=form_data.email)
        mock_verify_password.assert_called_once_with(
            form_data.hashed_password, db_user.hashed_password
        )
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Password incorrect"
