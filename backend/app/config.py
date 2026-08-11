from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    app_name: str = "Clean Architecture Auth API"
    jwt_secret_key: str = "unsafe-dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: URL = URL.create(
        "postgresql+psycopg",
        username="raguser",
        password="raguser2026",
        host="localhost",
        port=5432,
        database="ragdb",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        arbitrary_types_allowed=True,
    )


settings = Settings()
