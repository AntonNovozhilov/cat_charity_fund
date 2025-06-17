from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Класс конфигурации настроек для ядра приложения.
    """

    title: str
    date_base_url: str
    secret: str

    class Config:
        env_file = ".env"


settings = Settings()
