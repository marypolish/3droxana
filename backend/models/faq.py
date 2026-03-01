from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

collection_name = "faq"

def serialize_faq(faq) -> dict:
    serialized = faq.copy()
    serialized["_id"] = str(faq["_id"])
    return serialized


async def get_all_faqs(db: AsyncIOMotorDatabase):
    faqs = await db[collection_name].find().to_list(1000)
    return [serialize_faq(faq) for faq in faqs]

async def get_faq_by_id(db: AsyncIOMotorDatabase, id: str):
    faq = await db[collection_name].find_one({"_id": ObjectId(id)})
    return serialize_faq(faq) if faq else None

async def create_faq(db: AsyncIOMotorDatabase, data: dict):
    result = await db[collection_name].insert_one(data)
    return str(result.inserted_id)

async def update_faq(db: AsyncIOMotorDatabase, id: str, data: dict):
    await db[collection_name].update_one({"_id": ObjectId(id)}, {"$set": data})

async def delete_faq(db: AsyncIOMotorDatabase, id: str):
    await db[collection_name].delete_one({"_id": ObjectId(id)})
