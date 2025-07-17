from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject

from .base import BaseCRUD


class ProjectCRUD(BaseCRUD):
    """Класс для объекта проектов. Для создания CRUD."""

    async def get_projects_by_completion_rate(self, session: AsyncSession) -> list:
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    (
                        func.julianday(CharityProject.close_date) -
                        func.julianday(CharityProject.create_date),
                        CharityProject.description,
                    ),
                ]
            )
            .where(CharityProject.close_date is not None)
            .order_by(
                (
                    func.julianday(CharityProject.close_date) -
                    func.julianday(CharityProject.create_date)
                )
            )
        )
        projects = projects.scalars().all()
        res = [
            (
                project.name,
                (
                    (project.close_date - project.create_date).days
                    if project.close_date and project.create_date
                    else None
                ),
                project.description,
            )
            for project in projects
        ]
        return res


project = ProjectCRUD(CharityProject)
