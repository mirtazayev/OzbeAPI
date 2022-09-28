from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Dto(BaseModel):
    pass


class GenericDto(BaseModel):
    id: int
