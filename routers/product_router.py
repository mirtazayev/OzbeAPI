import shutil

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Models.models import Product
from database.database_config import get_db
from schema.product_DTO import ProductDTO
from services import product_service

router = APIRouter(tags=['Product Router'], prefix="/product")


@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {'products': products}


@router.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    for product in products:
        if product.id == product_id:
            return product
    return {'status': f"Product not found with id : {product_id}"}


@router.post('/products-create')
def create_product(dto: ProductDTO = Depends(), db: Session = Depends(get_db)):
    return product_service.create(dto=dto, db=db)


@router.put("/products-update/{product_id}")
def update_product(
        product_id: int,
        dto: ProductDTO = Depends(),
        db: Session = Depends(get_db)
):
    data = ProductDTO(**dto.__dict__).dict(exclude_unset=True)
    if len(dto.image.filename):
        file_url = 'media/products/' + dto.image.filename
        with open(file_url, "wb") as buffer:
            shutil.copyfileobj(dto.image.file, buffer)
        data.update({'image': file_url})
    db.query(Product).filter(Product.id == product_id).update(data)
    db.commit()
    return f'Product is updated successfully'


@router.delete("/products-delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    for product in products:
        if product.id == product_id:
            db.delete(product)
            db.commit()
            return {'status': 'Product is deleted'}
    else:
        raise HTTPException(status_code=404, detail=f"Product not found with id : {product_id}")
