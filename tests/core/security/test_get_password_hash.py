import pytest
from app.core.security import get_password_hash

@pytest.mark.unit
def test_get_password_hash():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)
    
    assert isinstance(hashed_password, str)
    assert hashed_password != password
    assert len(hashed_password) > 0

@pytest.mark.unit
def test_get_password_hash_consistency():
    password = "mysecretpassword"
    hashed_password1 = get_password_hash(password)
    hashed_password2 = get_password_hash(password)
    
    assert hashed_password1 != hashed_password2
