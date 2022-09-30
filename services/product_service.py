import shutil

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from Models.models import Product
from schema.product_DTO import ProductDTO


def create(dto: ProductDTO, db: Session):
    data = dto.dict()
    product = Product(**data)
    if len(dto.image.filename):
        file_url = 'media/products/' + dto.image.filename
        with open(file_url, "wb") as buffer:
            shutil.copyfileobj(dto.image.file, buffer)
        data.update({'image': file_url})
        product = Product(**data)
        db.add(product)
        db.commit()
        db.refresh(product)
    return product


def get(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found with id : '{product_id}'")
    return product
