from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.configuration import DATABASE_URL

# Set up the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency for providing a database session to routes
def get_db():
    """Get a database session.

    :return: Database session
    """
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
