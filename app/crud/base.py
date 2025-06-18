from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_donation_user
from app.models.user import User


class BaseCRUD:
    """Базовый класс для crud."""

    def __init__(self, model):
        self.model = model

    async def create(
        self, data, session: AsyncSession, user: Optional[User] = None
    ):
        """Функция для создания объекта."""

        data_in = data.dict()
        new_obj = self.model(**data_in)
        if user:
            new_obj.user_id = user.id
        session.add(new_obj)
        await session.commit()
        await session.refresh(new_obj)
        return new_obj

    async def remove(self, obj_id: int, session: AsyncSession):
        """Функция для удаления объекта."""

        remove = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        remove = remove.scalars().first()
        await session.delete(remove)
        await session.commit()
        return remove

    async def get_multi(
            self,
            session: AsyncSession,
            user: Optional[User] = None):
        """Функция для получения всех объектов."""

        if user:
            result = await check_donation_user(user=user, session=session)
            return result
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def update(self, obj, obj_in, session: AsyncSession):
        """Функция для обновления объекта."""

        up_data = obj_in.dict(exclude_unset=True)
        for filed, value in up_data.items():
            setattr(obj, filed, value)
        await session.commit()
        await session.refresh(obj)
        return obj
