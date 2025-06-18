from fastapi import HTTPException
from fastapi_users import schemas
from pydantic import validator


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    password: str

    @validator("password")
    def len_password(value):
        if len(value) < 6:
            raise HTTPException(status_code=400, detail="Короткий пароль")
        return value


class UserUpdate(schemas.BaseUserUpdate):
    pass
