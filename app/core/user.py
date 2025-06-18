from typing import Union

from fastapi import Depends
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.users import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategi() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategi
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validation(
        self, password: str, user: Union[UserCreate, User]
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException("Пароль слишком короткий")
        if user.email in password:
            raise InvalidPasswordException(
                "Пароль не должен состоять из почты."
            )
        print(f"Пользователь {user.email} зарегистрирован.")


async def get_usermanager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_user = FastAPIUsers(
    get_user_manager=get_usermanager, auth_backends=[auth_backend]
)

current_user = fastapi_user.current_user(active=True)
current_superuser = fastapi_user.current_user(active=True, superuser=True)
