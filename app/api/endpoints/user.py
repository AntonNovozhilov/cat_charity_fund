from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_user
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

user_router = fastapi_user.get_users_router(UserRead, UserUpdate)
user_router.routes = [
    rout for rout in user_router.routes if rout.name != "users:delete_user"
]

router.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
)
