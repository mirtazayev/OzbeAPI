from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from Models.models import Users, Comment
from configs.auths import get_session_user
from database.database_config import get_db
from schema.comment_DTO import CommentCreateDTO
from services import comment_service

router = APIRouter(tags=['Comment Router'], prefix="/comment")


@router.get("/comments")
def get_comments(db: Session = Depends(get_db)):
    comments = db.query(Comment).all()
    return {'comments': comments}


@router.post("/comments-create/{post_id}")
def create_comment(
        product_id: int,
        dto: CommentCreateDTO = Body(),
        db: Session = Depends(get_db),
        session_user: Users = Depends(get_session_user)
):
    dto.product_id = product_id
    return comment_service.create(dto, db, session_user)


@router.get("/{comment_id}")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.get(comment_id, db)
