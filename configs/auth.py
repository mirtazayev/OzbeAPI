from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from simplejwt import jwt, Jwt
from sqlalchemy.orm import Session
from starlette import status

from database.database_config import get_db
from models.auth_models import Users
from services import auth_service
from services.auth_service import TokenData
from settings import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        user_id: str = payload.get('user_id')
        if not user_id:
            raise credentials_exception
        return TokenData(id=user_id)
    except Jwt:
        raise credentials_exception


def get_session_user(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)) -> Users:
    credentials_exception = HTTPException(
        detail={'error': 'Could not validate credentials'},
        headers={'WWW-Authenticate': 'Bearer'},
        status_code=status.HTTP_401_UNAUTHORIZED)

    token_data = verify_access_token(token, credentials_exception)

    session_user: Users = auth_service.session_user(db=db, token_data=token_data)

    if not session_user.is_active:
        raise HTTPException(
            detail={'error': 'User is inactive'},
            headers={'WWW-Authenticate': 'Bearer'},
            status_code=status.HTTP_401_UNAUTHORIZED)

    return session_user
