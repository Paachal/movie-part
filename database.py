import asyncio
from datetime import datetime
from pymongo import ReturnDocument
from pymongo.errors import BulkWriteError
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/movieDB?retryWrites=true&w=majority&appName=Cluster0")

# Access the specific database
db = client.get_database("movieDB")

# Access the collections within the database
users_collection = db.get_collection("users")
movies_collection = db.get_collection("movies")
comments_collection = db.get_collection("comments")
ratings_collection = db.get_collection("ratings")

async def insert_sample_data():
    users = [
        {
            "username": "user1",
            "email": "user1@example.com",
            "password": "hashedpassword1",
            "created_at": datetime(2023, 1, 1)
        },
        {
            "username": "user2",
            "email": "user2@example.com",
            "password": "hashedpassword2",
            "created_at": datetime(2023, 1, 2)
        },
        {
            "username": "user3",
            "email": "user3@example.com",
            "password": "hashedpassword3",
            "created_at": datetime(2023, 1, 3)
        }
    ]

    movies = [
        {
            "title": "Movie 1",
            "description": "Description of movie 1",
            "release_year": 2021,
            "created_by": "user1",
            "created_at": datetime(2023, 1, 1)
        },
        {
            "title": "Movie 2",
            "description": "Description of movie 2",
            "release_year": 2022,
            "created_by": "user2",
            "created_at": datetime(2023, 1, 2)
        }
    ]

    comments = [
        {
            "movie_id": "movie1",
            "text": "Great movie!",
            "created_by": "user2",
            "created_at": datetime(2023, 1, 1)
        },
        {
            "movie_id": "movie2",
            "text": "Not bad",
            "created_by": "user3",
            "created_at": datetime(2023, 1, 2)
        }
    ]

    ratings = [
        {
            "movie_id": "movie1",
            "rating": 5,
            "created_by": "user3",
            "created_at": datetime(2023, 1, 1)
        },
        {
            "movie_id": "movie2",
            "rating": 4,
            "created_by": "user1",
            "created_at": datetime(2023, 1, 2)
        }
    ]

    # Clear collections before inserting sample data
    await users_collection.delete_many({})
    await movies_collection.delete_many({})
    await comments_collection.delete_many({})
    await ratings_collection.delete_many({})

    # Insert sample data without _id fields
    try:
        await users_collection.insert_many(users)
        await movies_collection.insert_many(movies)
        await comments_collection.insert_many(comments)
        await ratings_collection.insert_many(ratings)
    except BulkWriteError as e:
        print(f"Bulk write error: {e.details}")

# Ensure the sample data is inserted when the module is run
if __name__ == "__main__":
    asyncio.run(insert_sample_data())
