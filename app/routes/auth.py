from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
import logging
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from deps import get_users_collection
from database import users_collection

router = APIRouter()

SECRET_KEY = a2e651dc4653b28184cb8770efbd4e68901d13dcd35a691a85e51a9d3fe5ccae
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(users_collection: AsyncIOMotorCollection, username: str) -> Optional[dict]:
    user = await users_collection.find_one({"username": username})
    return user

@router.post("/register", response_model=Token)
async def register(user: User, users_collection: AsyncIOMotorCollection = Depends(get_users_collection)):
    logging.info(f"Registering user: {user.dict()}")
    db_user = await get_user(users_collection, user.username)
    if db_user:
        logging.warning("Username already registered")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    await users_collection.insert_one(user_dict)
    access_token = create_access_token(data={"sub": user.username})
    logging.info("User registered successfully")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), users_collection: AsyncIOMotorCollection = Depends(get_users_collection)):
    logging.info(f"User login attempt: {form_data.username}")
    db_user = await get_user(users_collection, form_data.username)
    if not db_user or not verify_password(form_data.password, db_user["password"]):
        logging.warning("Invalid username or password")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )
    access_token = create_access_token(data={"sub": form_data.username})
    logging.info("User logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}
