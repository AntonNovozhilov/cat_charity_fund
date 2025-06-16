from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.charity_projects import CharityProject

from .base import BaseCRUD


class ProjectCRUD(BaseCRUD):
    pass


project = ProjectCRUD(CharityProject)
