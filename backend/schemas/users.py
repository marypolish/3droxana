from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str
    tgNick: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    tgNick: str | None = None
    email: EmailStr | None = None

class UserOut(UserBase):
    id: str = Field(..., alias="_id")

    model_config = {
        "from_attributes": True,
        "validate_by_name": True
    }
