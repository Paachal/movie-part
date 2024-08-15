
import os
from motor.motor_asyncio import AsyncIOMotorClient

# Get the MongoDB URI from environment variables
mongodb_uri = os.getenv("MONGODB_URI")

# Create a new MongoDB client and connect to the database
client = AsyncIOMotorClient(mongodb_uri)
db = client.get_database()  # This will connect to the specified database in the URI

# Access the 'movies' collection in the database
movies_collection = db.get_collection("movies")
