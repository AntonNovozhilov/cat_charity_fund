from fastapi import HTTPException, Depends
from app.crud.charity_projects import project
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.charity_projects import CharityProject
from sqlalchemy import select


async def check_project_exit(id: int, session: AsyncSession):
    obj = await session.execute(select(CharityProject).where(CharityProject.id==id))
    obj = obj.scalars().first()
    if obj is False:
        raise HTTPException(status_code=422, detail='Данного проекта нет в базе данных')
    return obj