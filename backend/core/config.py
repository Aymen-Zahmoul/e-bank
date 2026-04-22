from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "e-bnk API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "your-super-secret-key-keep-it-safe" # In production, use env var
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    GOOGLE_CLIENT_ID: Optional[str] = "YOUR_GOOGLE_CLIENT_ID"
    APPLE_CLIENT_ID: Optional[str] = "YOUR_APPLE_CLIENT_ID"

    model_config = {"env_file": ".env"}

settings = Settings()
