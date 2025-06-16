from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_projects import CharityProject
from app.models.donations import Donation
from app.models.users import User


async def check_project_exit(project_id: int, session: AsyncSession) -> CharityProject:
    obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    obj = obj.scalars().first()
    if obj is False:
        raise HTTPException(status_code=422, detail="Данного проекта нет в базе данных")
    return obj


async def check_donation_user(user: User, session: AsyncSession):
    obj = await session.execute(select(Donation).where(Donation.user_id == user.id))
    obj = obj.scalars().all()
    if obj is False:
        raise HTTPException(status_code=403, detail="У вас нет пожертвований.")
    return obj


async def check_invested_amount_project(project_id: int, session: AsyncSession):
    obj = await check_project_exit(project_id, session)
    if obj.invested_amount > 0:
        raise HTTPException(
            status_code=403,
            detail="Нельзя удалять проекты, в которые уже проинвестировали",
        )
    return obj


async def check_close_date_project(project_id: int, session: AsyncSession):
    obj = await check_project_exit(project_id, session)
    if obj.close_date is not None:
        raise HTTPException(status_code=403, detail="Нельзя удалять закрытые проекты")
    return obj
