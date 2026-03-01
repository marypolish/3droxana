from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

collection_name = "sessions"

def serialize_session(session) -> dict:
    session["_id"] = str(session["_id"])
    return session

async def get_all_sessions(db: AsyncIOMotorDatabase):
    sessions = await db[collection_name].find().to_list(1000)
    return [serialize_session(s) for s in sessions]

async def get_session_by_id(db: AsyncIOMotorDatabase, id: str):
    session = await db[collection_name].find_one({"_id": ObjectId(id)})
    return serialize_session(session) if session else None

async def create_session(db: AsyncIOMotorDatabase, data: dict):
    result = await db[collection_name].insert_one(data)
    return str(result.inserted_id)

async def update_session(db: AsyncIOMotorDatabase, id: str, data: dict):
    await db[collection_name].update_one({"_id": ObjectId(id)}, {"$set": data})

async def delete_session(db: AsyncIOMotorDatabase, id: str):
    await db[collection_name].delete_one({"_id": ObjectId(id)})

async def get_sessions_by_user(db: AsyncIOMotorDatabase, user_id: str):
    sessions = await db[collection_name].find({"userId": user_id}).sort("updatedAt", -1).to_list(100)
    return [serialize_session(s) for s in sessions]

