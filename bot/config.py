from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List

class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_USERNAME: str = ""
    CHANNEL_ID: str
    CHANNEL_URL: str
    ADMIN_IDS: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/milliy_dasturchi"
    SITE_URL: str = "https://milliydasturchi.uz"
    PROJECT_NAME: str = "Milliy Dasturchi"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def admin_ids(self) -> List[int]:
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]

settings = Settings()
