
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from database import comments_collection

router = APIRouter()

class Comment(BaseModel):
    movie_id: str
    user_id: str
    content: str
    parent_comment_id: str | None = None

class CommentInDB(Comment):
    id: str

def comment_helper(comment) -> dict:
    return {
        "id": str(comment["_id"]),
        "movie_id": comment["movie_id"],
        "user_id": comment["user_id"],
        "content": comment["content"],
        "parent_comment_id": comment["parent_comment_id"]
    }

@router.get("/{movie_id}", response_model=list[CommentInDB])
async def get_comments(movie_id: str):
    comments = await comments_collection.find({"movie_id": movie_id}).to_list(100)
    return [comment_helper(comment) for comment in comments]

@router.post("/", response_model=CommentInDB, status_code=201)
async def add_comment(comment: Comment):
    new_comment = await comments_collection.insert_one(comment.dict())
    created_comment = await comments_collection.find_one({"_id": new_comment.inserted_id})
    return comment_helper(created_comment)

@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: str):
    delete_result = await comments_collection.delete_one({"_id": ObjectId(comment_id)})
    if delete_result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail="Comment not found")
