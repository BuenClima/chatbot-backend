from pydantic import BaseModel


# Pydantic models for User
class UserBase(BaseModel):
    """UserBase schema class for user data."""

    email: str


# Pydantic models for UserCreate
class UserCreate(UserBase):
    """UserCreate schema class for creating a new user."""

    hashed_password: str


# Pydantic models for UserUpdate
class UserUpdate(BaseModel):
    """UserUpdate schema class for updating user data."""

    email: str = None


# Pydantic models for UserRepr
class UserRepr(BaseModel):
    """UserRepr schema class for serializing user data."""

    id: int
    email: str
    is_active: bool


# Pydantic models for User
class User(UserBase):
    """User schema class for user data."""

    id: int
    is_active: bool
    hashed_password: str = None

    class Config: # pylint: disable=too-few-public-methods
        """Config class for User schema."""

        orm_mode = True
