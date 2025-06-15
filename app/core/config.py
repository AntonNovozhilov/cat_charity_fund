from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str
    date_base_url: str
    secret: str

    class Config:
        env_file = ".env"


settings = Settings()
