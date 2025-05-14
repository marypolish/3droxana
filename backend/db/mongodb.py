from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import MONGODB_URI, DATABASE_NAME

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    client.close()
    print("Closed MongoDB connection.")

def get_database():
    return db
