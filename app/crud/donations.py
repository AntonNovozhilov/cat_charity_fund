from sqlalchemy import select
from app.core.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.donations import Donation
from .base import BaseCRUD



class DonationCRUD(BaseCRUD):
    pass

donation = DonationCRUD(Donation)
