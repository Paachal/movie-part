from pymongo import MongoClient

# MongoDB connection string. Replace <username>, <password>, and <cluster-url> with your actual MongoDB credentials and URL.
client = MongoClient("mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/movieDB?retryWrites=true&w=majority&appName=Cluster0")

# Access the specific database
db = client.get_database("movieDB")

# Access the collections within the database
users_collection = db.get_collection("users")
movies_collection = db.get_collection("movies")
comments_collection = db.get_collection("comments")
ratings_collection = db.get_collection("ratings")
