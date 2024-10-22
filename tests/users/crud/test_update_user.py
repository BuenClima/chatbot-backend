import pytest
from app.users.schemas import UserUpdate
from app.users.crud import update_user


# Should return the updated user
@pytest.mark.unit
def test_update_user_should_return_user(mock_db,fake_active_user):
    # Arrange
    user_update = UserUpdate(email="test@email.com")

    # Set up the mock to return the user when get_user_by_id is called
    mock_db.query.return_value.filter.return_value.first.side_effect = [fake_active_user, None]

    # Act
    user = update_user(mock_db, 1, user_update)

    # Assert
    assert user.email == user_update.email, "The email should match the updated email"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(fake_active_user)

# Should raise an exception when the user is not updated
@pytest.mark.unit
def test_update_user_should_raise_exception_when_user_not_updated(mock_db,fake_active_user):
    # Arrange
    user_update = UserUpdate(email="test@email.com")


    # Set up the mock to return the user when get_user_by_id is called
    mock_db.query.return_value.filter.return_value.first.side_effect = [fake_active_user, None]
    mock_db.commit.side_effect = Exception("Exception on updating the user!")

    # Act
    with pytest.raises(Exception) as e:
        update_user(mock_db, 1, user_update)

    assert str(e.value) == "500: Internal server error occurred", "An exception should be raised"
    mock_db.refresh.assert_not_called()
    mock_db.commit.assert_called_once()


