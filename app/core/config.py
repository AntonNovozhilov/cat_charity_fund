from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Класс конфигурации настроек для ядра приложения.
    """

    title: str = 'Название'
    date_base_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'secret'

    class Config:
        env_file = ".env"


settings = Settings()
