
from pydantic import BaseModel

class RatingCreate(BaseModel):
    movie_id: str
    rating: int

class RatingResponse(BaseModel):
    movie_id: str
    user_id: str
    rating: int
