from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter
from app.models.donations import Donation
from app.schemas.donations import DonationsBase, DonationsCreate, DonationsGetCreateUser, DotationsDB
from app.core.db import get_async_session
from app.core.users import current_user
from app.crud.donations import donation


route = APIRouter(tags=['donations'])

@route.post('/donation/', response_model=DonationsGetCreateUser)
async def create_donation(data: DonationsCreate, session: AsyncSession = Depends(get_async_session)):
    new_donation = await donation.create(data, session)
    return new_donation

@route.get('/donation', response_model=list[DotationsDB])
async def get_all_donations(session: AsyncSession = Depends(get_async_session)):
    result = await donation.get_multi(session)
    return result