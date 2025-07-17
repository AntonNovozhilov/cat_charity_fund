from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Класс конфигурации настроек для ядра приложения.
    """

    title: str = 'Название'
    date_base_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'secret'
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    universe_domain: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
