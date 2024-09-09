from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import BaseModel
from typing import Optional
from app.core.security import SECRET_KEY, ALGORITHM
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

MONGODB_URL = "mongodb+srv://paschal:.adgjmptwpaschal@cluster0.dx4v8.mongodb.net/movieDB?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.movieDB

def get_database() -> AsyncIOMotorDatabase:
    return db

class User(BaseModel):
    username: str
    email: Optional[str] = None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        db = get_database()
        user = await db["users"].find_one({"username": username})
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return User(**user)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependency to get the users collection
def get_users_collection(db: AsyncIOMotorDatabase = Depends(get_database)):
    return db["users"]

# Dependency to get the movies collection
def get_movies_collection(db: AsyncIOMotorDatabase = Depends(get_database)):
    return db["movies"]

# Dependency to get the comments collection
def get_comments_collection(db: AsyncIOMotorDatabase = Depends(get_database)):
    return db["comments"]

# Dependency to get the ratings collection
def get_ratings_collection(db: AsyncIOMotorDatabase = Depends(get_database)):
    return db["ratings"]
