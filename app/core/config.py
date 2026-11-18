from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./app.db"
    session_cookie_name: str = "session_token"
    session_ttl: timedelta = timedelta(days=7)
    session_cookie_secure: bool = False


settings = Settings()
