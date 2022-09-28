from datetime import datetime

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    username: str
    password: str


class UserLoginDTO(BaseModel):
    username: str
    password: str


class UserDTO(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
