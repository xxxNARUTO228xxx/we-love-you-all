from pydantic import BaseModel, Field
import fastapi_users
import uuid


class UserModel(fastapi_users.schemas.BaseUser[uuid.UUID]):
    name: str = Field(default=None)


class UserCreate(fastapi_users.schemas.BaseUserCreate):
    name: str = Field(default=None)


class UserUpdate(UserModel, fastapi_users.schemas.BaseUserUpdate):
    pass