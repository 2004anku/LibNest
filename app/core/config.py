from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LibNest API"
    environment: str = "development"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "libnest"
    jwt_secret_key: str = "replace-with-a-long-random-secret"
    jwt_access_token_minutes: int = 30
    jwt_refresh_token_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

