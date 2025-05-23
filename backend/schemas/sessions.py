from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Message(BaseModel):
    role: str  # "user" або "assistant"
    text: str

class SessionBase(BaseModel):
    userId: str
    name: str  # нове поле
    messages: List[Message]
    createdAt: datetime
    updatedAt: datetime

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    messages: List[Message]
    updatedAt: datetime

class SessionOut(SessionBase):
    id: str = Field(..., alias="_id")

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }
