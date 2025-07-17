from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_projects import project
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    "",
    response_model=list[list[str]],
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_service: Aiogoogle = Depends(get_service),
):
    """
    Толкьо для суперпользователей.
    """
    result = await project.get_projects_by_completion_rate(session=session)
    spreadsheet_id = await spreadsheets_create(wrapper_service)
    await set_user_permissions(spreadsheet_id, wrapper_service)
    await spreadsheets_update_value(spreadsheet_id, wrapper_service, result)
    return result
