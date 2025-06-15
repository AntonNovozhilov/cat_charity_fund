from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectsBase(BaseModel):
    name: str = Field(max_length=100)
    description: str
    full_amount: int = Field(gt=0)


class ProjectCreate(ProjectsBase):
    pass


class ProjectUpdate(ProjectsBase):
    pass


class ProjectDB(BaseModel):
    id: int
    invested_amount: int
    fully_invested: bool = Field(default=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
