# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.database import db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate):
    user = await db["users"].find_one({"username": user_in.username})
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    hashed_password = get_password_hash(user_in.password)
    user = User(username=user_in.username, hashed_password=hashed_password)
    await db["users"].insert_one(user.dict())
    return UserResponse(username=user_in.username)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db["users"].find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
