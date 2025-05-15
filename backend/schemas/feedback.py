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

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }

