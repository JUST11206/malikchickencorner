# import os
# from dotenv import load_dotenv

# # Load .env variables
# load_dotenv()


# class Config:

#     SECRET_KEY = os.getenv("SECRET_KEY","malik_chicken_corner_secret_key")

#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# import os
# from dotenv import load_dotenv

# load_dotenv()


# class Config:

#     SECRET_KEY = os.getenv("SECRET_KEY")

#     # WhatsApp
#     WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
#     PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
#     OWNER_WHATSAPP = os.getenv("OWNER_WHATSAPP")    
import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Flask
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "malik_chicken_corner_secret_key"
    )

    # TiDB Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 1800
        }
    # WhatsApp Cloud API
    WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    OWNER_WHATSAPP = os.getenv("OWNER_WHATSAPP")