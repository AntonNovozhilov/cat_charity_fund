from sqlalchemy import Column, String, Text

from app.models.base import ModelBase


class CharityProject(ModelBase):
    """Модель для проектов."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
