from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.users import User


async def check_project_exit(project_id: int, session: AsyncSession) -> CharityProject:
    obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    obj = obj.scalars().first()
    if obj is False:
        raise HTTPException(status_code=422, detail="Данного проекта нет в базе данных")
    return obj


async def get_instance_open(model, session: AsyncSession):
    result = await session.execute(select(model).where(model.close_date == None))
    result = result.scalars().all()
    return result


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
            status_code=400,
            detail="Нельзя удалять проекты, в которые уже проинвестировали",
        )
    return obj

async def check_invested_amount_all(project_id: int, session: AsyncSession):
    obj = await check_project_exit(project_id, session)
    if obj.invested_amount == obj.full_amount:
        raise HTTPException(
            status_code=400,
            detail="Нельзя редактировать проекты, в которые уже проинвестировали",
        )
    return obj


async def check_close_date_project(project_id: int, session: AsyncSession):
    obj = await check_project_exit(project_id, session)
    if obj.fully_invested:
        raise HTTPException(status_code=400, detail="Нельзя редактировать закрытые проекты")
    return obj


async def check_upgrade_amount_project(project_id: int, session: AsyncSession):
    obj = await check_project_exit(project_id, session)
    invested_amount = obj.invested_amount
    obj_new = await check_project_exit(project_id, session)
    full_amount = obj_new.full_amount
    if full_amount < invested_amount:
        raise HTTPException(status_code=400, detail="Нельзя уменьшать сумму ниже внесенной")
    return obj