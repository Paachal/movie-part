# app/routes/movies.py
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from typing import List
from app.models import Movie, User
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse
from app.deps import get_current_user
from app.database import db

router = APIRouter()

@router.post("/", response_model=MovieResponse)
async def add_movie(movie_in: MovieCreate, current_user: User = Depends(get_current_user)):
    movie = Movie(**movie_in.dict(), added_by=current_user.id)
    await db["movies"].insert_one(movie.dict())
    return movie

@router.get("/", response_model=List[MovieResponse])
async def list_movies():
    movies = await db["movies"].find().to_list(100)
    return [Movie(**movie) for movie in movies]

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str):
    movie = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return Movie(**movie)

@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: str, movie_in: MovieUpdate, current_user: User = Depends(get_current_user)):
    movie = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    if not movie or movie["added_by"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to edit this movie")
    await db["movies"].update_one({"_id": ObjectId(movie_id)}, {"$set": movie_in.dict(exclude_unset=True)})
    updated_movie = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    return Movie(**updated_movie)

@router.delete("/{movie_id}")
async def delete_movie(movie_id: str, current_user: User = Depends(get_current_user)):
    movie = await db["movies"].find_one({"_id": ObjectId(movie_id)})
    if not movie or movie["added_by"] != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this movie")
    await db["movies"].delete_one({"_id": ObjectId(movie_id)})
    return {"detail": "Movie deleted successfully"}
