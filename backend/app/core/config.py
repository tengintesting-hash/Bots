from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = ""
    webapp_url: str = ""
    backend_public_url: str = ""
    admin_token: str = ""
    postback_secret: str = ""
    log_level: str = "INFO"
    cors_origins: str = ""
    database_path: str = "/data/database.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
