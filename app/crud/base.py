from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.users import current_user
from app.models.charity_projects import CharityProject
from app.models.donations import Donation
from app.models.users import User


class BaseCRUD:

    def __init__(self, model):
        self.model = model

    async def create(self, data, session: AsyncSession, user: Optional[User]):
        data_in = data.dict()
        if user:
            data_in["user_id"] = user.id
        new_obj = self.model(**data_in)
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def remove(self, id: int, session: AsyncSession):
        remove = await session.execute(select(self.model).where(self.model.id == id))
        remove = remove.scalars().first()
        await session.delete(remove)
        await session.commit()
        return remove

    async def get_multi(self, session: AsyncSession):
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def update(self, obj, obj_in, session: AsyncSession):
        up_data = obj_in.dict(exclude_unset=True)
        for filed, value in up_data.items():
            setattr(obj, filed, value)
        await session.commit()
        await session.refresh(obj)
        return obj
