import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables
DATABASE_URL = os.getenv("DATABASE_URL")
ACCESS_JWT_SECRET = os.getenv("ACCESS_JWT_SECRET")
REFRESH_JWT_SECRET = os.getenv("REFRESH_JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS= int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
