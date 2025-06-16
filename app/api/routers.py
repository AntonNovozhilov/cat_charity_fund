from fastapi import APIRouter

from .endpoints import users, project, dotaton

main_router = APIRouter()
main_router.include_router(users)
main_router.include_router(project)
main_router.include_router(dotaton)
