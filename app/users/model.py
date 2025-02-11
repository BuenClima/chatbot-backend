from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base): # pylint: disable=too-few-public-methods
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.email}>"
