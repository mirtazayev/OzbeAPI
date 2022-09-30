from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship

from Models.shared.base_models import BaseModel
from database.database_config import Base


class Users(BaseModel, Base):
    __tablename__ = 'user'
    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    username: str = Column(String(length=100), index=False)
    password: str = Column(String(length=300))
    is_active: bool = Column(Boolean, server_default='True')


class Comment(BaseModel):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    product = relationship('Product', back_populates='wishlist', cascade='all, delete, delete-orphan')

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('user', back_populates='wishlist', cascade='all, delete, delete-orphan')


class Wishlist(BaseModel):
    __tablename__ = 'wishlist'
    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    product = relationship('Product', back_populates='wishlist', cascade='all, delete, delete-orphan')

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('user', back_populates='wishlist', cascade='all, delete, delete-orphan')


class Category(BaseModel):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)

    product = relationship('Product', back_populates='category', cascade='all, delete, delete-orphan')


class Product(BaseModel):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True)
    price = Column(Float(2), nullable=False)
    description = Column(Text)
    addition_data = Column(JSON)
    quantity = Column(Integer, default=0)
    in_stock = Column(Boolean)

    images = relationship('ProductImage', back_populates='product', cascade='all, delete, delete-orphan')
    wishlist = relationship('Wishlist', back_populates='product', cascade='all, delete, delete-orphan')
    comment = relationship('Comment', back_populates='product', cascade='all, delete, delete-orphan')

    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    category = relationship('Category', back_populates='product', cascade='all, delete, delete-orphan')


class ProductImage(BaseModel, Base):
    __tablename__ = 'product_images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    product = relationship('Product', back_populates='images', cascade='all, delete, delete-orphan')
