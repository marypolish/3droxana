from fastapi import APIRouter, Depends, HTTPException
from ..db.mongodb import get_database
from ..models import sessions as session_model
from ..schemas import sessions as session_schema

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])

@router.get("/", response_model=list[session_schema.SessionOut])
async def read_all_sessions(db=Depends(get_database)):
    return await session_model.get_all_sessions(db)

@router.get("/{id}", response_model=session_schema.SessionOut)
async def read_session(id: str, db=Depends(get_database)):
    session = await session_model.get_session_by_id(db, id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# @router.post("/", response_model=str)
# async def create_session(session: session_schema.SessionCreate, db=Depends(get_database)):
#     return await session_model.create_session(db, session.dict())

@router.post("/", response_model=str)
async def create_or_update_session(session: session_schema.SessionCreate, db=Depends(get_database)):
    existing = await db["sessions"].find_one({
        "userId": session.userId,
        "name": session.name
    })

    # Сконвертувати messages (Pydantic) у plain dicts
    new_messages_dicts = [m.dict() for m in session.messages]

    if existing:
        # Об’єднати старі повідомлення (можливо dict-список) із новими
        combined_messages = existing.get("messages", []) + new_messages_dicts

        await db["sessions"].update_one(
            {"_id": existing["_id"]},
            {
                "$set": {
                    "messages": combined_messages,
                    "updatedAt": session.updatedAt or datetime.utcnow()
                }
            }
        )
        return str(existing["_id"])

    # Якщо не існує — створити нову сесію
    session_data = session.dict()
    session_data["messages"] = new_messages_dicts  # Перезаписати серіалізованими dict

    return await session_model.create_session(db, session_data)


@router.put("/{id}", response_model=session_schema.SessionOut)
async def update_session(id: str, session: session_schema.SessionUpdate, db=Depends(get_database)):
    await session_model.update_session(db, id, session.dict())
    updated = await session_model.get_session_by_id(db, id)
    if not updated:
        raise HTTPException(status_code=404, detail="Session not found after update")
    return updated

@router.delete("/{id}")
async def delete_session(id: str, db=Depends(get_database)):
    await session_model.delete_session(db, id)
    return {"message": "Session deleted successfully"}
