from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/movieDB?retryWrites=true&w=majority&appName=Cluster0")

# Access the specific database
db = client.movieDB
