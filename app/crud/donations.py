from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_donation_user
from app.core.db import get_async_session
from app.core.users import current_user
from app.models.donations import Donation
from app.models.users import User

from .base import BaseCRUD


class DonationCRUD(BaseCRUD):

    async def get_donation_me(
        self,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
    ):
        don = await check_donation_user(user=user, session=session)
        return don


donation = DonationCRUD(Donation)
