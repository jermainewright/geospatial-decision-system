from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Texas Supermarket Site Intelligence API"
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8081
    default_population_weight: float = 0.5
    default_road_weight: float = 0.3
    default_competition_weight: float = 0.2
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
