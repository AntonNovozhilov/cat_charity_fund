from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_invested_amount_all,
                                check_invested_amount_project,
                                check_project_exit, check_unique_name,
                                check_upgrade_amount_project)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_projects import project
from app.models.donation import Donation
from app.schemas.charity_projects import (ProjectCreate, ProjectDB,
                                          ProjectUpdate)
from app.services.investing import invest

route = APIRouter()


@route.post(
    "/",
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project_schema: ProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> ProjectDB:
    """
    Только для суперюзеров.\n
    Создаёт благотворительный проект.
    """

    await check_unique_name(project_schema.name, session)
    new_project = await project.create(project_schema, session)
    await invest(new_project, Donation, session)
    return new_project


@route.get("/", response_model=list[ProjectDB])
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[ProjectDB]:
    """Возвращает список всех проектов."""

    result = await project.get_multi(session)
    return result


@route.delete(
    "/{project_id}",
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> ProjectDB:
    """
    Только для суперюзеров.\n
    Удаляет проект. Нельзя удалить проект,\n
    в который уже были инвестированы средства, его можно только закрыть.
    """

    project_remove = await check_invested_amount_project(project_id, session)
    project_remove = await project.remove(project_id, session)
    return project_remove


@route.patch(
    "/{project_id}",
    response_model=ProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj: ProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> ProjectDB:
    """
    Только для суперюзеров.\n
    Закрытый проект нельзя редактировать;\n
    нельзя установить требуемую сумму меньше уже вложенной.
    """

    ex_project = await check_project_exit(project_id, session)
    await check_invested_amount_all(ex_project)
    await check_unique_name(obj.name, session)
    new_project = await project.update(ex_project, obj, session)
    await check_upgrade_amount_project(ex_project, new_project)
    return new_project
