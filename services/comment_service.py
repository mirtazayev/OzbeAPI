from fastapi import HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session
from starlette import status

from models.auth_models import Users
from models.product_models import Comment
from schema.comment_DTO import CommentCreateDTO
from services import product_service


def create(dto: CommentCreateDTO, db: Session, session_user: Users):
    product_service.get(dto.product_id, db)
    comments = Comment(**dto.dict())
    comments.product_id = dto.product_id
    comments.created_by = session_user.id
    db.add(comments)
    db.commit()
    db.refresh(comments)
    return comments


def get(comment_id: int, db: Session):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment not found with id: '{comment_id}'")
    return Response(status_code=status.HTTP_200_OK, content=comment)
