from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Класс конфигурации настроек для ядра приложения.
    """

    title: str = Field(..., env="TITLE")
    date_base_url: str = Field(..., env="DATE_BASE_URL")
    secret: str = Field(..., env="SECRET")

    class Config:
        env_file = ".env"


settings = Settings()
