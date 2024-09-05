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

