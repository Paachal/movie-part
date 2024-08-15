
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from database import ratings_collection

router = APIRouter()

class Rating(BaseModel):
    movie_id: str
    user_id: str
    rating: float

class RatingInDB(Rating):
    id: str

def rating_helper(rating) -> dict:
    return {
        "id": str(rating["_id"]),
        "movie_id": rating["movie_id"],
        "user_id": rating["user_id"],
        "rating": rating["rating"]
    }

@router.get("/{movie_id}", response_model=list[RatingInDB])
async def get_ratings(movie_id: str):
    ratings = await ratings_collection.find({"movie_id": movie_id}).to_list(100)
    return [rating_helper(rating) for rating in ratings]

@router.post("/", response_model=RatingInDB, status_code=201)
async def add_rating(rating: Rating):
    new_rating = await ratings_collection.insert_one(rating.dict())
    created_rating = await ratings_collection.find_one({"_id": new_rating.inserted_id})
    return rating_helper(created_rating)

@router.delete("/{rating_id}", status_code=204)
async def delete_rating(rating_id: str):
    delete_result = await ratings_collection.delete_one({"_id": ObjectId(rating_id)})
    if delete_result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail="Rating not found")
