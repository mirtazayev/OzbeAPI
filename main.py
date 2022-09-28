import shutil

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from configs.auth import get_session_user
from database.database_config import get_db, Base, engine
from models.auth_models import Users
from models.product_models import Product, Comment
from schema.auth_DTO import UserLoginDTO
from schema.comment_DTO import CommentCreateDTO
from schema.product_DTO import ProductDTO
from services import auth_service, product_service, comment_service
from services.auth_service import create

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/products", tags=['product'])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {'products': products}


@app.get("/products/{product_id}", tags=['product'])
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    for product in products:
        if product.id == product_id:
            return product
    return {'status': f"Product not found with id : {product_id}"}


@app.post('/products-create', tags=['product'])
def create_product(dto: ProductDTO = Depends(), db: Session = Depends(get_db)):
    return product_service.create(dto=dto, db=db)


@app.put("/products-update/{product_id}", tags=['product'])
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


@app.delete("/products-delete/{product_id}", tags=['product'])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    for product in products:
        if product.id == product_id:
            db.delete(product)
            db.commit()
            return {'status': 'Product is deleted'}
    else:
        raise HTTPException(status_code=404, detail=f"Product not found with id : {product_id}")


@app.post('/register', tags=['auth'])
def register(dto: UserLoginDTO, db: Session = Depends(get_db)):
    return create(dto=dto, db=db)


@app.post('/login', tags=['auth'])
def login(dto: UserLoginDTO = Depends(), db: Session = Depends(get_db)):
    return auth_service.login(dto, db)


@app.get("/comments", tags=['comment'])
def get_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).all()
    return {'comments': comments}


@app.post("/comments-create", tags=['comment'])
def create_comment(dto: CommentCreateDTO,
                   db: Session = Depends(get_db),
                   session_user: Users = Depends(get_session_user)):
    return comment_service.create(dto, db, session_user)


@app.get("/{comment_id}", tags=['comment'])
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.get(comment_id, db)


if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, reload=True)
