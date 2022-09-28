from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from configs.auths import get_session_user
from database.database_config import get_db
from schema.auth_DTO import UserLoginDTO, UserDTO
from services import auth_service
from services.auth_service import create, TokenData

router = APIRouter(tags=['Auth Router'], prefix="/auth")


@router.post('/register')
def register(dto: UserLoginDTO, db: Session = Depends(get_db)):
    return create(dto=dto, db=db)


@router.post('/login')
def login(dto: UserLoginDTO = Depends(), db: Session = Depends(get_db)):
    return auth_service.login(dto, db)


@router.get('/me', response_model=UserDTO)
def login(db: Session = Depends(get_db), session_user: TokenData = Depends(get_session_user)):
    return auth_service.session_user(db, session_user)
