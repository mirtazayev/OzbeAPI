from schema import Dto


class CommentCreateConfig(Dto):
    class Config:
        schema_extra = {
            "example":
                {
                    "message": "Comment"
                }
        }
        orm_mode = True
