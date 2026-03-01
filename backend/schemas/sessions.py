from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    role: str  # "user" або "assistant"
    text: str

class SessionBase(BaseModel):
    userId: str
    name: str  # нове поле
    messages: Optional[List[Message]] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class SessionCreate(BaseModel):
    userId: str
    name: str
    messages: list[Message]
    updatedAt: Optional[datetime] = None

class SessionUpdate(BaseModel):
    messages: List[Message]
    updatedAt: datetime

class SessionOut(SessionBase):
    id: str = Field(..., alias="_id")

    model_config = {
        "from_attributes": True,
        "allow_population_by_field_name": True
    }
