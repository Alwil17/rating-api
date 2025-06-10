from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # Application
    APP_NAME: str = "RatingAPI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    APP_SECRET_KEY: str = "super_secret_key"
    APP_DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DB_ENGINE: str = "sqlite"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "ratings"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # OAuth
    OAUTH_CLIENT_ID: str = ""
    OAUTH_CLIENT_SECRET: str = ""

    # Sentry
    SENTRY_DSN: str = ""

    # Prometheus
    PROMETHEUS_ENABLED: bool = True


settings = Settings()
