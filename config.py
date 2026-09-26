from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.0-flash"

    image_provider: str = "placeholder"

    hf_api_key: str | None = None
    hf_image_model: str = "stabilityai/stable-diffusion-xl-base-1.0"

    app_name: str = "ComicCraft"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()