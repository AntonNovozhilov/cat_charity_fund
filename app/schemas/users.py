from fastapi_users import schemas
from pydantic import Field, validator
from fastapi import HTTPException


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    password: str

    @validator('password')
    def len_password(value):
        if len(value) < 6:
            raise HTTPException(status_code=400, detail='Короткий пароль')
        return value



class UserUpdate(schemas.BaseUserUpdate):
    pass
