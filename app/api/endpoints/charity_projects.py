from fastapi import APIRouter, Depends
from app.crud.charity_projects import project
from app.schemas.charity_projects import ProjectCreate, ProjectDB, ProjectUpdate
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession




route = APIRouter(tags=['charity_projects'])

@route.post('/charity_project/', response_model=ProjectDB)
async def create_charity_project(project_schema: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    new_project =  await project.create_project(project_schema, session)
    return new_project

@route.get('/', response_model=list[ProjectDB])
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    result = await project.get_multi(session)
    return result

@route.delete('/charity_project/{project_id}', response_model=ProjectDB)
async def delete_charity_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    project_remove = await project.remove_project(id=project_id, session=session)
    return project_remove
