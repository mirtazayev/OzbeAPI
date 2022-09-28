from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    username: str
    password: str


class UserLoginDTO(BaseModel):
    username: str
    password: str
