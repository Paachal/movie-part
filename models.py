# app/models.py
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    hashed_password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Movie(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    added_by: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Rating(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: PyObjectId
    user_id: PyObjectId
    rating: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Comment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: PyObjectId
    user_id: PyObjectId
    content: str
    parent_comment_id: Optional[PyObjectId] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
