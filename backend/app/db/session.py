from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings
from .base import db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print(f"Connected to MongoDB: {settings.DATABASE_NAME}")

async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")