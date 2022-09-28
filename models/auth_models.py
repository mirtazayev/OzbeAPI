from sqlalchemy import Column, Integer, String, Boolean

from database.database_config import Base
from models.shared.base_models import BaseModel


class Users(BaseModel, Base):
    __tablename__ = 'user'
    id: int = Column(Integer, primary_key=True, unique=True, index=True, nullable=False)
    username: str = Column(String(length=100), index=False)
    password: str = Column(String(length=300))
    is_active: bool = Column(Boolean, server_default='True')
