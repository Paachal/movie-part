from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# MongoDB connection details
MONGODB_URL = "mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/movieDB?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.movieDB

# Define collection references
users_collection = db["users"]
movies_collection = db["movies"]
comments_collection = db["comments"]
ratings_collection = db["ratings"]
