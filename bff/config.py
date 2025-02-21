from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    API_URL: str
    UUID_URL: str
    AUTH_TOKEN: str
    REQ_TIMEOUT: int
