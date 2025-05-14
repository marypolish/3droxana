from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class FAQBase(BaseModel):
    question: str
    answer: str
    keywords: List[str]
    category: str
    subcategory: str
    source: Optional[str]
    tags: List[str]
    visible: bool = True

class FAQCreate(FAQBase):
    pass

class FAQUpdate(FAQBase):
    pass

class FAQOut(FAQBase):
    id: str = Field(..., alias="_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
