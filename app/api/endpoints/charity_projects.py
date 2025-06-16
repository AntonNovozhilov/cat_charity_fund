from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_close_date_project,
    check_invested_amount_project,
    check_project_exit,
)
from app.core.db import get_async_session
from app.core.users import current_seperuser
from app.crud.charity_projects import project
from app.schemas.charity_projects import ProjectCreate, ProjectDB, ProjectUpdate

route = APIRouter(tags=["charity_projects"])


@route.post(
    "/charity_project/",
    response_model=ProjectDB,
    dependencies=[Depends(current_seperuser)],
)
async def create_charity_project(
    project_schema: ProjectCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект.
    """

    new_project = await project.create(project_schema, session)
    return new_project


@route.get("/", response_model=list[ProjectDB])
async def get_all_charity_projects(session: AsyncSession = Depends(get_async_session)):
    """Возвращает список всех проектов."""

    result = await project.get_multi(session)
    return result


@route.delete(
    "/charity_project/{project_id}",
    response_model=ProjectDB,
    dependencies=[Depends(current_seperuser)],
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы средства, его можно только закрыть.
    """

    project_remove = await check_invested_amount_project(id=project_id, session=session)
    project_remove = await project.remove(id=project_id, session=session)
    return project_remove


@route.patch(
    "/charity_project/{project_id}",
    response_model=ProjectDB,
    dependencies=[Depends(current_seperuser)],
)
async def update_charity_project(
    project_id: int,
    obj: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму меньше уже вложенной.
    """

    ex_project = await check_project_exit(project_id, session)
    ex_project = await check_close_date_project(project_id, session)
    new_project = await project.update(ex_project, obj, session)
    return new_project
