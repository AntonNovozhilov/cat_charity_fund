from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationsBase(BaseModel):
    full_amount: int = Field(gt=0)
    comment: Optional[str]


class DonationsCreate(DonationsBase):
    pass

    class Config:
        schema_extra = {
            'example': {
                'full_amount': 100,
                'comment': 'Первое пожертвование',
            }
        }


class DonationsGetCreateUser(DonationsBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DotationsDB(DonationsBase):
    id: int
    create_date: datetime
    # user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
