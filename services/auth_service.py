import datetime

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic.schema import timedelta
from simplejwt import jwt
from sqlalchemy.orm import Session
from starlette import status
from typing import Optional

from models.auth_models import Users
from schema.auth_DTO import UserLoginDTO
from services import utils
from settings import settings


class TokenData(BaseModel):
    id: Optional[str] = None


def generate_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({
        'exp': expiry, })
    encoded_token = jwt.encode(settings.secret_key, settings.algorithm)
    return encoded_token


def create(dto: UserLoginDTO, db: Session):
    user = Users(**dto.dict())
    user.password = utils.encode_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(dto: UserLoginDTO, db: Session):
    user = db.query(Users).filter(Users.username == dto.username).first()

    if not user:
        raise HTTPException(
            detail={"error": f"User not found by given username :{dto.username} "},
            status_code=status.HTTP_404_NOT_FOUND)

    if not utils.match_password(dto.password, user.password):
        raise HTTPException(
            detail={'error': 'Password entered incorrect'},
            status_code=status.HTTP_400_BAD_REQUEST)
    token = generate_access_token(data={'user_id': user.id})
    return {'access_token': token, "token_type": "Bearer", "status": "successfully entered"}


def session_user(db: Session, token_data: TokenData):
    return db.query(Users).filter(Users.id == token_data.id).first()
