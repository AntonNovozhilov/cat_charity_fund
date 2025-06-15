from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text

from app.core.db import Base


class Donation(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id"))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
