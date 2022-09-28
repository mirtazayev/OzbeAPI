from sqlalchemy import Column, Integer, String, Boolean, Text, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.database_config import Base
from models.shared.base_models import BaseModel


class Category(BaseModel, Base):
    __tablename__ = 'category'
    id: int = Column(Integer, primary_key=True)
    title: str = Column(Text)

    product = relationship('Product', back_populates='category', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return self.title


class Comment(BaseModel, Base):
    __tablename__ = 'comment'
    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    message: str = Column(String(100))
    product_id: int = Column(Integer, ForeignKey('product.id'))

    # comment = relationship('Product', back_populates='comment', cascade='all, delete, delete-orphan')

    created_by: int = Column(Integer, ForeignKey('user.id'), nullable=False)


class Product(BaseModel, Base):
    __tablename__ = 'product'
    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    title: str = Column(Text)
    price: float = Column(Float)
    image = Column(String)
    description: str = Column(String(length=350))
    in_stock: bool = Column(Boolean)
    tag: str = Column(Text)

    comment = relationship("Comment", cascade="all")

    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))
    category = relationship('Category', back_populates="product")

    # comment_id = Column(Integer, ForeignKey('comment.id', ondelete='CASCADE'))
    # comment = relationship('Comment', back_populates="comment")

    def __repr__(self):
        return self.title
