from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import ModelBase


class Donation(ModelBase):
    """Модель для пожертвований."""

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    comment = Column(Text)
