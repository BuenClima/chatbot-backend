import pytest
from app.core.security import create_tokens


@pytest.mark.unit
def test_create_tokens(mock_create_access_token, mock_create_refresh_token):
    user_id = 1
    mock_create_access_token.return_value = "mock_access_token"
    mock_create_refresh_token.return_value = "mock_refresh_token"

    tokens = create_tokens(user_id)

    assert tokens["access_token"] == "mock_access_token"
    assert tokens["refresh_token"] == "mock_refresh_token"
    mock_create_access_token.assert_called_once_with(data={"sub": str(user_id)})
    mock_create_refresh_token.assert_called_once_with(data={"sub": str(user_id)})
