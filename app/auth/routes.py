from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.users import schemas
from app.auth import service as authservice, schemas as authschemas

# Create a router for authentication-related routes
router = APIRouter()


# Route for signing up (creating a new user)
@router.post("/signup", response_model=authschemas.AuthBase)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> authschemas.AuthBase:
    """Sign up a new user.

    :param user: UserCreate
    :param db: Session
    :return: AuthBase
    :rtype: AuthBase
    """
    return authservice.sign_up_user(user, db)


# Route for signing in (generating an access token)
@router.post("/signin", response_model=authschemas.AuthBase)
def login_for_access_token(
    form_data: authschemas.AuthSignIn, db: Session = Depends(get_db)
) -> authschemas.AuthBase:
    """Sign in a user.

    :param form_data: AuthSignIn
    :param db: Session
    :return: AuthBase
    :rtype: AuthBase
    """
    return authservice.sign_in_user(form_data, db)
