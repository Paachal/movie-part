
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List
from app.models import Comment, User
from app.schemas.comment import CommentCreate, CommentResponse
from app.deps import get_current_user
from app.database import db

router = APIRouter()

@router.post("/", response_model=CommentResponse)
async def add_comment(comment_in: CommentCreate, current_user: User = Depends(get_current_user)):
    comment = Comment(**comment_in.dict(), user_id=current_user.id)
    await db["comments"].insert_one(comment.dict())
    return comment

@router.get("/{movie_id}", response_model=List[CommentResponse])
async def get_comments(movie_id: str):
    comments = await db["comments"].find({"movie_id": ObjectId(movie_id)}).to_list(100)
    return [Comment(**comment) for comment in comments]
