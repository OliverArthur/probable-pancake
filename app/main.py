from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import authentication, post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(authentication.router, prefix="/api/v1")
