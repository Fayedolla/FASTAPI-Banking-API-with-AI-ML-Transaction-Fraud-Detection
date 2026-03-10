from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
# from pathlib import Path

# env_path = Path(__file__).parent.parent.parent.parent / ".envs" / ".env.local"
env_path = "../../.envs/.env.local"


class Settings(BaseSettings):
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    model_config = SettingsConfigDict(
        env_file=env_path, env_ignore_empty=True, extra="ignore"
    )

    API_V1_STR: str = ""
    PROJECT_NAME: str = ""
    PROJECT_DESCRIPTION: str = ""
    SITE_NAME: str = ""
    DATABASE_URL: str = ""
    MAIL_FROM: str = ""
    MAIL_FROM_NAME: str = ""
    SMTP_HOST: str = "mailpit"
    SMTP_PORT: int = 1025
    MAILPIT_UI_PORT: int = 8025
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"


settings = Settings()
