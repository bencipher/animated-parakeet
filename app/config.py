from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    env_name: str = "local"
    base_url: str
    consumer_key: str
    consumer_secret: str
    bearer_token: str
    access_token: str
    access_token_secret: str

    class Config:
        env_file = ".env"


class ProductionSettings(Settings):
    env_name: str = "production"
    base_url: str = "https://production.example.com"

    class Config:
        env_file = "prod.env"


class StagingSettings(Settings):
    env_name: str = "staging"
    base_url: str = "https://staging.example.com"

    class Config:
        env_file = "staging.env"


@lru_cache
def get_settings(env: str = None) -> Settings:
    if env:
        if env.lower() == "production":
            settings = ProductionSettings()
        elif env.lower() == "staging":
            settings = StagingSettings()
        else:
            settings = Settings()
    else:
        settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
