from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donations import donation
from app.models.charity_project import CharityProject
from app.models.user import User
from app.schemas.donations import (DonationsCreate, DonationsGetCreateUser,
                                   DotationsDB)
from app.services.investing import invest

route = APIRouter()


@route.post("/", response_model=DonationsGetCreateUser)
async def create_donation(
    data: DonationsCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> DonationsGetCreateUser:
    """Сделать пожертвование."""

    new_donation = await donation.create(data, session, user)
    await invest(new_donation, CharityProject, session)
    return new_donation


@route.get(
    "/",
    response_model=list[DotationsDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
) -> list[DotationsDB]:
    """
    Только для суперюзеров.\n
    Возвращает список всех пожертвований.
    """

    result = await donation.get_multi(session)
    return result


@route.get("/my", response_model=list[DonationsGetCreateUser])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[DonationsGetCreateUser]:
    """Вернуть список пожертвований пользователя, выполняющего запрос."""

    result = await donation.get_multi(session, user)
    return result
