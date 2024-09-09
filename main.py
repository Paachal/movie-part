from fastapi import FastAPI
from app.routes import auth, movies, ratings, comments

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(movies.router, prefix="/movies", tags=["movies"])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API"}
