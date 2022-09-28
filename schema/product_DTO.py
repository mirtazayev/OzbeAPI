from fastapi import UploadFile, File
from pydantic import BaseModel, validator


class ProductDTO(BaseModel):
    title: str
    price: float
    image: UploadFile or None = File(None)
    description: str
    tag: str
    in_stock: bool


class ProductUpdateDTO(BaseModel):
    title: str
    description: str

    @validator("title")
    def valid_title(cls, v):
        if not v:
            raise ValueError('Title Cannot be null')
        if v.isspace():
            raise ValueError('Title Cannot be blank')
        return v.title()

    @validator("description")
    def valid_body(cls, v: str):
        if not v:
            raise ValueError('Description or body Cannot be null')
        if v.isspace():
            raise ValueError('Description cannot be blank')
        return v

    class Config:
        orm_mode = True
