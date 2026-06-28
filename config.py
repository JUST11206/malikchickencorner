import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY","malik_chicken_corner_secret_key")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False