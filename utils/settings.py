from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="CipherChest")
    database_url: str = Field(default="sqlite:///./app.db")
    secret_key: str = Field(default="super-secret-key")
    jwt_secret_key: str = Field(default="change-me")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_minutes: int = Field(default=60 * 24 * 7)
    csrf_secret: str = Field(default="csrf-secret")
    inactivity_lock_minutes: int = Field(default=15)
    rate_limit: str = Field(default="20/minute")
    encryption_master_key: str = Field(default="01234567890123456789012345678901")
    attachments_dir: str = Field(default="attachments")
    backup_dir: str = Field(default="backups")
    log_file: str = Field(default="security.log")
    hibp_api_url: str = Field(default="https://api.pwnedpasswords.com/range/")
    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    smtp_host: str | None = None
    smtp_port: int | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_sender: str | None = None
    admin_email: str = Field(default="admin@local")
    admin_password: str = Field(default="ChangeMe123!")

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
