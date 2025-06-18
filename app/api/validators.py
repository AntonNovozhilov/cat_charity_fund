from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User


async def check_project_exit(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка наличия обхекста в базе данных."""

    obj = await session.execute(
        select(CharityProject).where(CharityProject.id == project_id)
    )
    obj = obj.scalars().first()
    if obj is False:
        raise HTTPException(
            status_code=422, detail="Данного проекта нет в базе данных"
        )
    return obj


async def check_unique_name(
    name: str, session: AsyncSession
) -> CharityProject:
    """Проверка уникальности поля name."""

    obj = await session.execute(
        select(CharityProject).where(CharityProject.name == name)
    )
    obj = obj.scalars().first()
    if obj:
        raise HTTPException(
            status_code=400, detail="Имя должно быть уникальным"
        )
    return obj


async def check_donation_user(user: User, session: AsyncSession):
    """Проверка пользователя для GET запроса."""

    obj = await session.execute(
        select(Donation).where(Donation.user_id == user.id)
    )
    obj = obj.scalars().all()
    if obj is False:
        raise HTTPException(status_code=403, detail="У вас нет пожертвований.")
    return obj


async def check_invested_amount_project(
    project_id: int, session: AsyncSession
):
    """Проверка проекта на положительное поле invested_amount."""

    obj = await check_project_exit(project_id, session)
    if obj.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалять проекты, в которые уже проинвестировали",
        )
    return obj


async def check_invested_amount_all(project: CharityProject):
    """Проверка проекта на заверенность."""

    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail="""Нельзя редактировать проекты,\n
            в которые уже проинвестировали""",
        )
    return project


async def check_upgrade_amount_project(
    project: CharityProject, new_project: CharityProject
):
    """Проверка проекта на измененное поле full_amount."""

    if new_project.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=400, detail="Нельзя уменьшать сумму ниже внесенной"
        )
    return new_project
