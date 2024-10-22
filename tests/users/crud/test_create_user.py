import pytest
from app.users.model import User
from app.users.schemas import UserCreate
from app.core.security import get_password_hash
from unittest.mock import ANY
from app.users.crud import create_user


# Should return the user
@pytest.mark.unit
def test_create_user_should_return_user(mock_db):
    # Arrange
    user_create = UserCreate(email="test@example.com", hashed_password="password")
    hashed_password = get_password_hash(user_create.hashed_password)
    expected_user = User(email=user_create.email, hashed_password=hashed_password)

    # Set up the mock to return None when first is called, simulating that the user does not exist
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # Act
    user = create_user(mock_db, user_create)

    # Assert
    assert (
        user.email == expected_user.email
    ), "The email should match the expected email"
    mock_db.add.assert_called_once_with(ANY)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)


# Should raise an exeption when the user is not created
@pytest.mark.unit
def test_create_user_should_raise_exception_when_user_not_created(mock_db):
    # Arrange
    user_create = UserCreate(email="test@example.com", hashed_password="password")

    # Set up the mock to return None when first is called, simulating that the user does not exist
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_db.add.side_effect = Exception("Exeption on adding the user!")

    # Act
    with pytest.raises(Exception) as e:
        create_user(mock_db, user_create)

    assert (
        str(e.value) == "500: Internal server error occurred"
    ), "An exception should be raised"
    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()
