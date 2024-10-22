from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.users import crud, schemas
from app.auth import schemas as authschemas
from app.core import security

# Function to sign up a user
def sign_up_user(user: schemas.UserCreate, db: Session) -> authschemas.AuthBase:
    """Sign up a new user.

    :param user: User data
    :type user: schemas.UserCreate
    :param db: Database session
    :type db: Session
    :return: AuthBase object
    :rtype: dict
    """
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = crud.create_user(db=db, user=user)

    tokens = security.create_tokens(db_user.id)

    return authschemas.AuthBase(
        tokens=tokens,
        token_type="bearer",
        user=schemas.UserRepr(
            id=db_user.id, email=db_user.email, is_active=db_user.is_active
        ),
    )


# Function to sign in a user
def sign_in_user(
    form_data: authschemas.AuthSignIn, db: Session
) -> authschemas.AuthBase:
    """Sign in a user.

    :param form_data: User login data
    :type form_data: schemas.AuthSignIn
    :param db: Database session
    :type db: Session
    :return: User object
    :rtype: dict
    """
    user = crud.get_user_by_email(db, email=form_data.email)

    if not user:
        raise HTTPException(
            status_code=401, detail="Email not registered, sign up first"
        )

    if not security.verify_password(form_data.hashed_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password incorrect")

    tokens = security.create_tokens(user.id)

    return authschemas.AuthBase(
        tokens=tokens,
        token_type="bearer",
        user=schemas.UserRepr(id=user.id, email=user.email, is_active=user.is_active),
    )
