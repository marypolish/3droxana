from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

class FeedbackBase(BaseModel):
    userId: str
    message: str
    submittedAt: datetime
    status: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    message: Optional[str] = None
    status: Optional[str] = None

class FeedbackOut(FeedbackBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
