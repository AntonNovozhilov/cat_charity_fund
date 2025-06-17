from datetime import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session


async def get_instance_open(model, session: AsyncSession):
    """Получение объектов которые еще не закрыты."""

    result = await session.execute(
        select(model).where(model.close_date.is_(None)))
    result = result.scalars().all()
    return result


async def invest(
        obj,
        model,
        session: AsyncSession = Depends(get_async_session)):
    """Процесс инвестирования."""

    iterabels = await get_instance_open(model, session)
    if not iterabels:
        return obj
    for iter in iterabels:
        obj_amount = obj.full_amount - obj.invested_amount
        iter_amount = iter.full_amount - iter.invested_amount
        if iter_amount > obj_amount:
            obj.invested_amount = obj.full_amount
            obj.close_date = datetime.now()
            obj.fully_invested = True
            iter.invested_amount += obj_amount
        elif iter_amount < obj_amount:
            obj.invested_amount += iter_amount
            iter.invested_amount = iter.full_amount
            iter.close_date = datetime.now()
            iter.fully_invested = True
        else:
            obj.invested_amount = obj.full_amount
            obj.close_date = datetime.now()
            obj.fully_invested = True
            iter.invested_amount = iter.full_amount
            iter.close_date = datetime.now()
            iter.fully_invested = True
    await session.commit()
    await session.refresh(obj)
    await session.refresh(iter)
