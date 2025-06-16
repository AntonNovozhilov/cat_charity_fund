from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectsBase(BaseModel):
    name: str = Field(max_length=100)
    description: str
    full_amount: int = Field(gt=0)


class ProjectCreate(ProjectsBase):
    pass

    class Config:
        schema_extra = {
            'example': {
                'name': 'Project 1',
                'description': 'Первый проект',
                'full_amount': 100000,
            }
        }

class ProjectUpdate(ProjectsBase):
    pass


class ProjectDB(ProjectsBase):
    id: int
    invested_amount: int = Field(default=0)
    fully_invested: bool = Field(default=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
