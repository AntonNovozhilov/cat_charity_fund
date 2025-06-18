from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class ProjectsBase(BaseModel):
    """Базовая схема для проектов."""

    name: str = Field(title='Имя', min_length=5, max_length=100)
    description: str = Field(title='Описание', min_length=5)
    full_amount: PositiveInt = Field(title='Сумма сбора')


class ProjectCreate(ProjectsBase):
    """Схема для создания проектов."""

    class Config:
        schema_extra = {
            "example": {
                "name": "Project 1",
                "description": "Первый проект",
                "full_amount": 100000,
            }
        }
        title = 'Создание проекта'


class ProjectUpdate(BaseModel):
    """Схема для обновления проектов."""

    name: Optional[str] = Field(
        None,
        title='Имя',
        min_length=5,
        max_length=100
    )
    description: Optional[str] = Field(None, title='Описание', min_length=5)
    full_amount: Optional[PositiveInt] = Field(None, title='Сумма сбора')

    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "name": "Project 100",
                "description": "Сотый проект",
                "full_amount": 10005555,
            }
        }
        title = 'Обновление проекта'


class ProjectDB(ProjectsBase):
    """Схема для возврата обхекта из БД."""

    id: int
    invested_amount: int = Field(title='Внесенная сумма', default=0)
    fully_invested: bool = Field(
        title='Булево значение закрыт/открыт проект',
        default=False
    )
    create_date: datetime = Field(title='Дата создания')
    close_date: Optional[datetime] = Field(title='Дата закрытия')

    class Config:
        orm_mode = True
        title = 'Проект (ответ из БД).'
