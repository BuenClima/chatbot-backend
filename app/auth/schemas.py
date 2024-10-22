from pydantic import BaseModel
from app.users import schemas

class AuthTokens(BaseModel):
    """AuthTokens schema class for authentication-related routes.

    :param BaseModel: Pydantic BaseModel
    """

    access_token: str
    refresh_token: str


class AuthBase(BaseModel):
    """AuthBase schema class for authentication-related routes.

    :param BaseModel: Pydantic BaseModel
    :type BaseModel: Pydantic BaseModel
    """

    tokens: AuthTokens
    token_type: str
    user: schemas.UserRepr



class AuthSignIn(BaseModel):
    """AuthSignIn schema class for authentication-related routes.

    :param BaseModel: Pydantic BaseModel
    """

    email: str
    hashed_password: str
