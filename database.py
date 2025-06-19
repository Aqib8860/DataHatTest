from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()


MONGO_DB_URL = os.environ.get("MONGODB_URL")
DB_NAME = os.environ.get("DB_NAME")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(MONGO_DB_URL)
    app.database = app.mongodb_client[DB_NAME]

    # Redis setup
    redis_client = redis.from_url(REDIS_URL, decode_responses=False)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")


    yield
    app.mongodb_client.close()
    await redis_client.close()

def get_database(request: Request):
    return request.app.database
