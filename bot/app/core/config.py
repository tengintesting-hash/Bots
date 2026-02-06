from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = ""
    bot_username: str = ""
    webapp_url: str = ""
    backend_public_url: str = ""
    log_level: str = "INFO"
    database_path: str = "/data/database.db"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
