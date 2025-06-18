from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationsBase(BaseModel):
    """Базовый класс схем пожертвований."""

    full_amount: PositiveInt = Field(title='Cумма пожертвования')
    comment: Optional[str] = Field(title='Комментарий')


class DonationsCreate(DonationsBase):
    """Класс схемы для создания пожертвований."""

    class Config:
        schema_extra = {
            "example": {
                "full_amount": 100,
                "comment": "Первое пожертвование",
            }
        }
        title = 'Создание пожертвований'


class DonationsGetCreateUser(DonationsBase):
    """Класс схемы для получения пожертвований."""

    id: int
    create_date: datetime = Field(title='Дата создания')

    class Config:
        orm_mode = True
        title = 'Получение пожертвований пользователя'


class DotationsDB(DonationsBase):
    """Класс схемы для обхекта пожертвований."""

    id: int
    create_date: datetime = Field(title='Дата создания')
    user_id: int = Field(title='id пользователя')
    invested_amount: int = Field(title='Распределенная сумма пожертвований')
    fully_invested: bool = Field(title='Булево значение открыто/закрыто')
    close_date: Optional[datetime] = Field(title='Дата закрытия')

    class Config:
        orm_mode = True
        title = 'Получение объекта пожертвований из БД'
