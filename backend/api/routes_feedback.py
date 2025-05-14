from fastapi import APIRouter, Depends, HTTPException
from ..db.mongodb import get_database
from ..models import feedback as feedback_model
from ..schemas import feedback as feedback_schema

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

@router.get("/", response_model=list[feedback_schema.FeedbackOut])
async def read_all_feedback(db=Depends(get_database)):
    return await feedback_model.get_all_feedback(db)

@router.get("/{id}", response_model=feedback_schema.FeedbackOut)
async def read_feedback(id: str, db=Depends(get_database)):
    feedback = await feedback_model.get_feedback_by_id(db, id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.post("/", response_model=str)
async def create_feedback(feedback: feedback_schema.FeedbackCreate, db=Depends(get_database)):
    return await feedback_model.create_feedback(db, feedback.dict())

@router.put("/{id}")
async def update_feedback(id: str, feedback: feedback_schema.FeedbackUpdate, db=Depends(get_database)):
    await feedback_model.update_feedback(db, id, feedback.dict())
    return {"message": "Feedback updated successfully"}

@router.delete("/{id}")
async def delete_feedback(id: str, db=Depends(get_database)):
    await feedback_model.delete_feedback(db, id)
    return {"message": "Feedback deleted successfully"}
