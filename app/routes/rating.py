
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List
from app.models import Rating, User
from app.schemas.rating import RatingCreate, RatingResponse
from app.deps import get_current_user
from app.database import db

router = APIRouter()

@router.post("/", response_model=RatingResponse)
async def rate_movie(rating_in: RatingCreate, current_user: User = Depends(get_current_user)):
    rating = Rating(**rating_in.dict(), user_id=current_user.id)
    await db["ratings"].insert_one(rating.dict())
    return rating

@router.get("/{movie_id}", response_model=List[RatingResponse])
async def get_movie_ratings(movie_id: str):
    ratings = await db["ratings"].find({"movie_id": ObjectId(movie_id)}).to_list(100)
    return [Rating(**rating) for rating in ratings]
