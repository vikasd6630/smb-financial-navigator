import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GCP_PROJECT_ID = os.getenv("TODO_GCP_PROJECT_ID")
    GCP_LOCATION = os.getenv("TODO_GCP_LOCATION")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

settings = Settings()