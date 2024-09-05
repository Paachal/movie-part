from fastapi import APIRouter, Depends
from app.deps import get_ratings_collection
from pymongo.collection import Collection
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_ratings(ratings_collection: Collection = Depends(get_ratings_collection)):
    ratings = await ratings_collection.find().to_list(100)
    return ratings

@router.post("/")
async def create_rating(rating: dict, ratings_collection: Collection = Depends(get_ratings_collection)):
    result = await ratings_collection.insert_one(rating)
    return {"_id": str(result.inserted_id)}
