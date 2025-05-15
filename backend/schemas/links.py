from pydantic import BaseModel, Field
from typing import List, Optional

class LinkBase(BaseModel):
    title: str
    url: str
    description: str
    category: str
    tags: List[str]
    visible: bool = True

class LinkCreate(LinkBase):
    pass

class LinkUpdate(LinkBase):
    pass

class LinkOut(LinkBase):
    id: str = Field(..., alias="_id")

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }
