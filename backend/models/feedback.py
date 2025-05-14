from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

collection_name = "feedback"

def serialize_feedback(feedback) -> dict:
    feedback["_id"] = str(feedback["_id"])
    feedback["submittedAt"] = feedback["submittedAt"].strftime("%Y-%m-%dT%H:%M:%SZ")
    return feedback

async def get_all_feedback(db: AsyncIOMotorDatabase):
    feedbacks = await db[collection_name].find().to_list(1000)
    return [serialize_feedback(feedback) for feedback in feedbacks]

async def get_feedback_by_id(db: AsyncIOMotorDatabase, id: str):
    feedback = await db[collection_name].find_one({"_id": ObjectId(id)})
    return serialize_feedback(feedback) if feedback else None

async def create_feedback(db: AsyncIOMotorDatabase, data: dict):
    data["submittedAt"] = datetime.utcnow()  # Автоматично додаємо поточну дату та час
    result = await db[collection_name].insert_one(data)
    return str(result.inserted_id)

async def update_feedback(db: AsyncIOMotorDatabase, id: str, data: dict):
    if "submittedAt" in data:
        data["submittedAt"] = datetime.utcnow()  # Оновлюємо дату подачі при оновленні
    await db[collection_name].update_one({"_id": ObjectId(id)}, {"$set": data})

async def delete_feedback(db: AsyncIOMotorDatabase, id: str):
    await db[collection_name].delete_one({"_id": ObjectId(id)})
