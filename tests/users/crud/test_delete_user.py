
import pytest
from app.users.model import User
from unittest.mock import ANY
from app.users.crud import delete_user


# Should return the deleted user
@pytest.mark.unit
def test_delete_user_should_return_user(mock_db, fake_active_user):
    # Set up the mock to return the user when get_user_by_id is called
    mock_db.query.return_value.filter.return_value.first.return_value = fake_active_user

    # Act
    user = delete_user(mock_db, 1)

    # Assert
    assert user == fake_active_user, "The user should be returned"
    mock_db.delete.assert_called_once_with(fake_active_user)
    mock_db.commit.assert_called_once()

# Should raise an exception when the user is not deleted
@pytest.mark.unit
def test_delete_user_should_raise_exception_when_user_not_deleted(mock_db, fake_active_user):
    # Set up the mock to return the user when get_user_by_id is called
    mock_db.query.return_value.filter.return_value.first.return_value = fake_active_user
    mock_db.commit.side_effect = Exception("Exception on deleting the user!")

    # Act
    with pytest.raises(Exception) as e:
        delete_user(mock_db, 1)

    assert str(e.value) == "500: Internal server error occurred", "An exception should be raised"
    mock_db.commit.assert_called_once()
    mock_db.delete.assert_called_once_with(fake_active_user)

