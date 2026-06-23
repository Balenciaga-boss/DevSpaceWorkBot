from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    admin_chat_id: int = Field(alias="ADMIN_CHAT_ID")
    database_url: str = Field(alias="DATABASE_URL")
    timezone: str = Field(default="Europe/Bucharest", alias="TIMEZONE")
    spam_cooldown_seconds: int = Field(default=60, alias="SPAM_COOLDOWN_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

