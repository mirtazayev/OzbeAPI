from pydantic import validator

from configs.comment_config import CommentCreateConfig


class CommentCreateDTO(CommentCreateConfig):
    product_id: int
    message: str

    @validator('message')
    def comment_message(cls, arg: str):
        if not arg:
            raise ValueError('Message Cannot be null')
        return arg
