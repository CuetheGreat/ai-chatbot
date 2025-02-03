from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import DB
from app.routers.userRouter import router
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    DB.connect()

app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
