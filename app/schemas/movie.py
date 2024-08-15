
from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    description: str

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class MovieResponse(BaseModel):
    title: str
    description: str
    added_by: str
