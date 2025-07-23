import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GCP_PROJECT_ID = os.getenv("semiotic-sylph-466615-u2")
    GCP_LOCATION = os.getenv("us-west1")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

settings = Settings()