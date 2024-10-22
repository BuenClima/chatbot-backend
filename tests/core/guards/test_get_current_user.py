from unittest.mock import patch
import pytest
from fastapi import HTTPException
from jose import JWTError
from app.core.guards import get_current_user, ACCESS_JWT_SECRET, ALGORITHM


@pytest.mark.unit
def test_get_current_user_success(mock_db, fake_active_user):
    token = "fake_token"
    with patch(
        "app.core.guards.jwt.decode", return_value={"sub": fake_active_user.id}
    ) as mock_decode, patch(
        "app.users.crud.get_user_by_id", return_value=fake_active_user
    ) as mock_get_user_by_id:

        result = get_current_user(token=token, db=mock_db)

        mock_decode.assert_called_once_with(
            token, ACCESS_JWT_SECRET, algorithms=[ALGORITHM]
        )
        mock_get_user_by_id.assert_called_once_with(
            mock_db, user_id=fake_active_user.id
        )

        assert result.id == fake_active_user.id
        assert result.email == fake_active_user.email
        assert result.is_active == fake_active_user.is_active


@pytest.mark.unit
def test_get_current_user_invalid_token(mock_db):
    token = "fake_token"
    with patch("app.core.guards.jwt.decode", side_effect=JWTError) as mock_decode:
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=mock_db)

        mock_decode.assert_called_once_with(
            token, ACCESS_JWT_SECRET, algorithms=[ALGORITHM]
        )
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"


def test_get_current_user_user_not_found(mock_db):
    token = "fake_token"
    with patch(
        "app.core.guards.jwt.decode", return_value={"sub": 1}
    ) as mock_decode, patch(
        "app.users.crud.get_user_by_id", return_value=None
    ) as mock_get_user_by_id:

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=mock_db)

        mock_decode.assert_called_once_with(
            token, ACCESS_JWT_SECRET, algorithms=[ALGORITHM]
        )
        mock_get_user_by_id.assert_called_once_with(mock_db, user_id=1)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"


@pytest.mark.unit
def test_get_current_user_no_user_id(mock_db):
    token = "fake_token"
    with patch("app.core.guards.jwt.decode", return_value={}) as mock_decode:
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=token, db=mock_db)

        mock_decode.assert_called_once_with(
            token, ACCESS_JWT_SECRET, algorithms=[ALGORITHM]
        )
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"
