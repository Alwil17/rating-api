from app.config import Settings as BaseSettings
from pydantic_settings import BaseSettings

class TestSettings(BaseSettings):
    """Test-specific settings that override the base settings"""
    APP_NAME: str = "RatingAPI-Test"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "test"
    APP_SECRET_KEY: str = "test_secret_key"
    APP_DEBUG: bool = True

    # Override database settings to use SQLite
    DB_ENGINE: str = "sqlite"
    DATABASE_URL: str = "sqlite:///:memory:"
    
    # Override JWT settings for faster tests
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    JWT_ALGORITHM: str = "HS256"
    
    # Testing-specific settings
    TESTING: bool = True

# Create an instance of the test settings
test_settings = TestSettings()
