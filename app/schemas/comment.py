
from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    movie_id: str
    content: str
    parent_comment_id: Optional[str] = None

class CommentResponse(BaseModel):
    movie_id: str
    user_id: str
    content: str
    parent_comment_id: Optional[str] = None
