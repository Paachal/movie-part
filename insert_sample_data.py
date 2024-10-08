import asyncio
from datetime import datetime
from pymongo.errors import BulkWriteError
from database import get_database

async def insert_sample_data():
    db = get_database()
    users_collection = db.get_collection("users")
    movies_collection = db.get_collection("movies")
    comments_collection = db.get_collection("comments")
    ratings_collection = db.get_collection("ratings")

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
            "created_by": None,
            "created_at": datetime(2023, 1, 1)
        },
        {
            "title": "Movie 2",
            "description": "Description of movie 2",
            "release_year": 2022,
            "created_by": None,
            "created_at": datetime(2023, 1, 2)
        }
    ]

    comments = [
        {
            "movie_id": None,
            "text": "Great movie!",
            "created_by": None,
            "created_at": datetime(2023, 1, 1)
        },
        {
            "movie_id": None,
            "text": "Not bad",
            "created_by": None,
            "created_at": datetime(2023, 1, 2)
        }
    ]

    ratings = [
        {
            "movie_id": None,
            "rating": 5,
            "created_by": None,
            "created_at": datetime(2023, 1, 1)
        },
        {
            "movie_id": None,
            "rating": 4,
            "created_by": None,
            "created_at": datetime(2023, 1, 2)
        }
    ]

    # Clear collections before inserting sample data
    await users_collection.delete_many({})
    await movies_collection.delete_many({})
    await comments_collection.delete_many({})
    await ratings_collection.delete_many({})

    # Insert sample data
    try:
        inserted_users = await users_collection.insert_many(users)
        user_ids = inserted_users.inserted_ids

        # Use inserted user IDs to create movie references
        user1_id = user_ids[0]
        user2_id = user_ids[1]
        user3_id = user_ids[2]

        movies[0]["created_by"] = user1_id
        movies[1]["created_by"] = user2_id

        inserted_movies = await movies_collection.insert_many(movies)
        movie_ids = inserted_movies.inserted_ids

        # Use inserted movie IDs to create comment and rating references
        movie1_id = movie_ids[0]
        movie2_id = movie_ids[1]

        comments[0]["movie_id"] = movie1_id
        comments[1]["movie_id"] = movie2_id
        comments[0]["created_by"] = user2_id
        comments[1]["created_by"] = user3_id

        ratings[0]["movie_id"] = movie1_id
        ratings[1]["movie_id"] = movie2_id
        ratings[0]["created_by"] = user3_id
        ratings[1]["created_by"] = user1_id

        await comments_collection.insert_many(comments)
        await ratings_collection.insert_many(ratings)
    except BulkWriteError as e:
        print(f"Bulk write error: {e.details}")

# Ensure the sample data is inserted when the module is run
if __name__ == "__main__":
    asyncio.run(insert_sample_data())
