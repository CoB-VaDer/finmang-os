from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "FinMang OS")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://finmang:finmang@localhost:5432/finmang")
    environment: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
