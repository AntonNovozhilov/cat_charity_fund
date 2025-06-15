from fastapi import APIRouter

from .endpoints import users

main_router = APIRouter()
main_router.include_router(users)
