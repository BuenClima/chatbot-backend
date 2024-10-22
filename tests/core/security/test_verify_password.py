import pytest
from bcrypt import hashpw, gensalt
from app.core.security import verify_password

@pytest.mark.unit
def test_verify_password_correct():
    plain_password = "securepassword"
    hashed_password = hashpw(plain_password.encode("utf-8"), gensalt()).decode("utf-8")
    assert verify_password(plain_password, hashed_password) == True

@pytest.mark.unit
def test_verify_password_incorrect():
    plain_password = "securepassword"
    hashed_password = hashpw("differentpassword".encode("utf-8"), gensalt()).decode("utf-8")
    assert verify_password(plain_password, hashed_password) == False

@pytest.mark.unit
def test_verify_password_empty():
    plain_password = ""
    hashed_password = hashpw("somepassword".encode("utf-8"), gensalt()).decode("utf-8")
    assert verify_password(plain_password, hashed_password) == False
