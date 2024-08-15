
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pydantic import BaseModel
from database import movies_collection

router = APIRouter()

class Movie(BaseModel):
    title: str
    director: str
    year: int
    genres: list
    rating: float

class MovieInDB(Movie):
    id: str

def movie_helper(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "director": movie["director"],
        "year": movie["year"],
        "genres": movie["genres"],
        "rating": movie["rating"]
    }

@router.get("/", response_model=list[MovieInDB])
async def get_movies():
    movies = await movies_collection.find().to_list(100)
    return [movie_helper(movie) for movie in movies]

@router.post("/", response_model=MovieInDB, status_code=201)
async def add_movie(movie: Movie):
    new_movie = await movies_collection.insert_one(movie.dict())
    created_movie = await movies_collection.find_one({"_id": new_movie.inserted_id})
    return movie_helper(created_movie)

@router.get("/{movie_id}", response_model=MovieInDB)
async def get_movie(movie_id: str):
    movie = await movies_collection.find_one({"_id": ObjectId(movie_id)})
    if movie:
        return movie_helper(movie)
    raise HTTPException(status_code=404, detail="Movie not found")

@router.put("/{movie_id}", response_model=MovieInDB)
async def update_movie(movie_id: str, movie: Movie):
    updated_movie = await movies_collection.find_one_and_update(
        {"_id": ObjectId(movie_id)},
        {"$set": movie.dict()},
        return_document=True
    )
    if updated_movie:
        return movie_helper(updated_movie)
    raise HTTPException(status_code=404, detail="Movie not found")

@router.delete("/{movie_id}", status_code=204)
async def delete_movie(movie_id: str):
    delete_result = await movies_collection.delete_one({"_id": ObjectId(movie_id)})
    if delete_result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail="Movie not found")
