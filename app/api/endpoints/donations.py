from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.users import current_seperuser, current_user
from app.crud.donations import donation
from app.models.donations import Donation
from app.models.users import User
from app.schemas.donations import (
    DonationsBase,
    DonationsCreate,
    DonationsGetCreateUser,
    DotationsDB,
)

route = APIRouter(tags=["donations"])


@route.post("/donation/", response_model=DonationsGetCreateUser)
async def create_donation(
    data: DonationsCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""

    new_donation = await donation.create(data, session, user)
    return new_donation


@route.get(
    "/donation",
    response_model=list[DotationsDB],
    dependencies=[Depends(current_seperuser)],
)
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    """
    Только для суперюзеров.\n
    Возвращает список всех пожертвований.
    """

    result = await donation.get_multi(session)
    return result


@route.get("/donattion/me", response_model=list[DonationsGetCreateUser])
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""

    result = await donation.get_donation_me(user, session)
    return result
