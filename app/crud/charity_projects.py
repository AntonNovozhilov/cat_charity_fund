from sqlalchemy import select
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.charity_projects import CharityProject
from fastapi.encoders import jsonable_encoder



class ProjectCRUD:

    def __init__(self, model):
        self.model = model

    async def get_multi(self, session: AsyncSession) -> list[CharityProject]:
        result = await session.execute(select(CharityProject))
        return result.scalars().all()

    async def create_project(self, data, session: AsyncSession) -> CharityProject:
        data_in = data.dict()
        new_progect = self.model(**data_in)
        session.add(new_progect)
        await session.commit()
        await session.refresh(new_progect)
        return new_progect
    
    async def remove_project(self, id: int, session: AsyncSession) -> CharityProject:
        project_remove = await session.execute(select(CharityProject).where(CharityProject.id == id))
        project_remove = project_remove.scalars().first()
        await session.delete(project_remove)
        await session.commit()
        return project_remove
    
    async def update_project(self, obj: CharityProject, obj_in, session: AsyncSession) -> CharityProject:
        up_data = obj_in.dict(exclude_unset=True)
        for filed, value in up_data.items():
            setattr(obj, filed, value)
        await session.commit()
        await session.refresh(obj)
        return obj


project = ProjectCRUD(CharityProject)
