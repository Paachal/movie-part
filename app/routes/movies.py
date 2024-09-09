from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorCollection
from deps import get_movies_collection
from database import movies_collection

router = APIRouter()

class Movie(BaseModel):
    title: str
    description: str
    release_year: int

@router.post("/", response_model=Movie)
async def create_movie(movie: Movie, movies_collection: AsyncIOMotorCollection = Depends(get_movies_collection)):
    movie_dict = movie.dict()
    await movies_collection.insert_one(movie_dict)
    return movie

@router.get("/", response_model=List[Movie])
async def get_movies(movies_collection: AsyncIOMotorCollection = Depends(get_movies_collection)):
    movies = await movies_collection.find().to_list(100)
    return movies
