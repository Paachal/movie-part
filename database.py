from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from datetime import datetime

client = AsyncIOMotorClient("mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/movieDB?retryWrites=true&w=majority&appName=Cluster0")

# Access the specific database
db = client.get_database("movieDB")

# Access the collections within the database
users_collection = db.get_collection("users")
movies_collection = db.get_collection("movies")
comments_collection = db.get_collection("comments")
ratings_collection = db.get_collection("ratings")

# Sample data
users = [
    {
        "_id": ObjectId("64dcbf1f1c4f4b6d1c8e4a1b"),
        "username": "user1",
        "email": "user1@example.com",
        "password": "hashedpassword1",
        "created_at": datetime(2023, 1, 1)
    },
    {
        "_id": ObjectId("64dcbf1f1c4f4b6d1c8e4a1c"),
        "username": "user2",
        "email": "user2@example.com",
        "password": "hashedpassword2",
        "created_at": datetime(2023, 1, 2)
    }
]

movies = [
    {
        "_id": ObjectId("64dcbf3a1c4f4b6d1c8e4a1d"),
        "title": "Inception",
        "description": "A mind-bending thriller by Christopher Nolan.",
        "release_date": datetime(2010, 7, 16),
        "genre": "Science Fiction",
        "created_by": ObjectId("64dcbf1f1c4f4b6d1c8e4a1b"),
        "created_at": datetime(2023, 1, 1)
    },
    {
        "_id": ObjectId("64dcbf3a1c4f4b6d1c8e4a1e"),
        "title": "The Dark Knight",
        "description": "A superhero film directed by Christopher Nolan.",
        "release_date": datetime(2008, 7, 18),
        "genre": "Action",
        "created_by": ObjectId("64dcbf1f1c4f4b6d1c8e4a1c"),
        "created_at": datetime(2023, 1, 2)
    }
]

comments = [
    {
        "_id": ObjectId("64dcbf591c4f4b6d1c8e4a1f"),
        "movie_id": ObjectId("64dcbf3a1c4f4b6d1c8e4a1d"),
        "user_id": ObjectId("64dcbf1f1c4f4b6d1c8e4a1b"),
        "comment": "Amazing movie!",
        "parent_comment_id": None,
        "created_at": datetime(2023, 1, 1, 12, 0, 0)
    },
    {
        "_id": ObjectId("64dcbf591c4f4b6d1c8e4a20"),
        "movie_id": ObjectId("64dcbf3a1c4f4b6d1c8e4a1e"),
        "user_id": ObjectId("64dcbf1f1c4f4b6d1c8e4a1c"),
        "comment": "Best Batman movie ever!",
        "parent_comment_id": None,
        "created_at": datetime(2023, 1, 2, 12, 0, 0)
    }
]

ratings = [
    {
        "_id": ObjectId("64dcbf701c4f4b6d1c8e4a21"),
        "movie_id": ObjectId("64dcbf3a1c4f4b6d1c8e4a1d"),
        "user_id": ObjectId("64dcbf1f1c4f4b6d1c8e4a1b"),
        "rating": 5,
        "created_at": datetime(2023, 1, 1, 13, 0, 0)
    },
    {
        "_id": ObjectId("64dcbf701c4f4b6d1c8e4a22"),
        "movie_id": ObjectId("64dcbf3a1c4f4b6d1c8e4a1e"),
        "user_id": ObjectId("64dcbf1f1c4f4b6d1c8e4a1c"),
        "rating": 4,
        "created_at": datetime(2023, 1, 2, 13, 0, 0)
    }
]

async def insert_sample_data():
    await users_collection.insert_many(users)
    await movies_collection.insert_many(movies)
    await comments_collection.insert_many(comments)
    await ratings_collection.insert_many(ratings)
    print("Sample data inserted successfully.")

# To run the async function
import asyncio
asyncio.run(insert_sample_data())
