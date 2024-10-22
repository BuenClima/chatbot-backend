import pytest
from app.users.model import User
from unittest.mock import ANY
from app.users.crud import get_user_by_id

# Should return the user when the user exists
@pytest.mark.unit
def test_get_user_by_id_should_return_user_when_user_exists(mock_db, fake_active_user):
    mock_db.query.return_value.filter.return_value.first.return_value = fake_active_user
    
    user = get_user_by_id(mock_db, 1)

    assert user == fake_active_user, "The user should be the same as the fake"
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_called_once_with(ANY)
    
    filter_call_args = mock_db.query.return_value.filter.call_args[0][0]
    assert str(filter_call_args) == str(User.id == 1)

# Should return None when the user does not exist
@pytest.mark.unit
def test_get_user_by_id_should_return_none_when_user_does_not_exist(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    user = get_user_by_id(mock_db, 1)

    assert user is None, "The user should be None"
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_called_once_with(ANY)
    
    filter_call_args = mock_db.query.return_value.filter.call_args[0][0]
    assert str(filter_call_args) == str(User.id == 1)
    
# Should raise an exception when an exception occurs
@pytest.mark.unit
def test_get_user_by_id_should_raise_exception_when_exception_occurs(mock_db):
    mock_db.query.side_effect = Exception("Exception on getting the user!")
    
    with pytest.raises(Exception) as e:
        get_user_by_id(mock_db, 1)
    
    assert str(e.value) == "500: Internal server error occurred", "An exception should be raised"
    mock_db.query.assert_called_once_with(User)
    mock_db.query.return_value.filter.assert_not_called()