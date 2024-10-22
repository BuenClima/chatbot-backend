import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.security import create_access_token
from app.core.configuration import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

@pytest.mark.unit
def test_create_access_token_with_default_expiry():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == "testuser"
    assert "exp" in decoded_token
    assert datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc) > datetime.now(timezone.utc)

@pytest.mark.unit
def test_create_access_token_with_custom_expiry():
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=10)
    token = create_access_token(data, expires_delta)
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    
    assert decoded_token["sub"] == "testuser"
    assert "exp" in decoded_token
    expected_expiry = datetime.now(timezone.utc) + expires_delta
    assert datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc) > datetime.now(timezone.utc)
    assert datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc) <= expected_expiry

@pytest.mark.unit
def test_create_access_token_with_empty_data():
    data = {}
    token = create_access_token(data)
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    
    assert "exp" in decoded_token
    assert datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc) > datetime.now(timezone.utc)
