from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from .config import settings


class Prebase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Prebase)

engine = create_async_engine(settings.date_base_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Генератор ассинхронной сессии."""

    async with AsyncSessionLocal() as async_session:
        yield async_session
