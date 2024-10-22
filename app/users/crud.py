from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.users.model import User
from app.users.schemas import UserCreate, UserUpdate
from app.core import security
from app.core.logger import logger


# Get user by email
def get_user_by_email(db: Session, email: str) -> User:
    """Get a user by email.

    :param db: Database session
    :type db: Session
    :param email: User email
    :type email: str
    :return: User object
    :rtype: User
    """
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.error("Error getting user by email: %s", e)
        raise HTTPException(
            status_code=500, detail="Internal server error occurred"
        ) from e


# Get user by ID
def get_user_by_id(db: Session, user_id: int) -> User:
    """Get a user by ID.

    :param db: Database session
    :type db: Session
    :param user_id: User ID
    :type user_id: int
    :return: User object
    :rtype: User
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        logger.error("Error getting user by ID: %s", e)
        raise HTTPException(
            status_code=500, detail="Internal server error occurred"
        ) from e


# Create a new user
def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user.

    :param db: Database session
    :type db: Session
    :param user: User data
    :type user: UserCreate
    :return: User object
    :rtype: User
    """
    try:
        hashed_password = security.get_password_hash(user.hashed_password)
        user_data = user.model_dump()
        user_data.update({"hashed_password": hashed_password})
        db_user = User(**user_data)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        logger.error("Error creating user: %s", e)
        raise HTTPException(
            status_code=500, detail="Internal server error occurred"
        ) from e


# Update user
def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    """Update a user.

    :param db: Database session
    :type db: Session
    :param user_id: User ID
    :type user_id: int
    :param user: User data
    :type user: UserUpdate
    :return: User object
    :rtype: User
    """
    try:
        db_user = get_user_by_id(db, user_id)
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        logger.error("Error updating user: %s", e)
        raise HTTPException(
            status_code=500, detail="Internal server error occurred"
        ) from e


# Delete user
def delete_user(db: Session, user_id: int) -> User:
    """Delete a user.

    :param db: Database session
    :type db: Session
    :param user_id: User ID
    :type user_id: int
    :return: User object
    :rtype: User
    """
    try:
        db_user = get_user_by_id(db, user_id)
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception as e:
        db.rollback()
        logger.error("Error deleting user: %s", e)
        raise HTTPException(
            status_code=500, detail="Internal server error occurred"
        ) from e
