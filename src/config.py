from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "cloro-ph-api"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/cloro_ph"
    log_level: str = "INFO"
    sentry_dsn: str = ""


settings = Settings()
