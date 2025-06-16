from fastapi import APIRouter

from .endpoints import dotaton, project, users

main_router = APIRouter()
main_router.include_router(users)
main_router.include_router(project)
main_router.include_router(dotaton)
