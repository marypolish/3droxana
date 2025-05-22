from fastapi import APIRouter, Depends, HTTPException
from ..db.mongodb import get_database
from ..models import users as user_model
from ..schemas import users as user_schema
from ..schemas.users import UserLogin

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/", response_model=list[user_schema.UserOut])
async def read_all_users(db=Depends(get_database)):
    return await user_model.get_all_users(db)

@router.get("/{id}", response_model=user_schema.UserOut)
async def read_user(id: str, db=Depends(get_database)):
    user = await user_model.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
async def login_user(login: UserLogin, db=Depends(get_database)):
    user = await user_model.get_user_by_credentials(db, login.email, login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Невірна пошта або пароль")
    return {"message": "Успішний вхід", "user": user}

@router.post("/register", response_model=str)
async def register_user(user: user_schema.UserCreate, db=Depends(get_database)):
    # Перевірка, чи email вже існує
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач з таким email вже існує")

    # Зберігаємо користувача без хешування пароля
    user_data = user.dict()
    return await user_model.create_user(db, user_data)

@router.put("/{id}")
async def update_user(id: str, user: user_schema.UserUpdate, db=Depends(get_database)):
    await user_model.update_user(db, id, {k: v for k, v in user.dict().items() if v is not None})
    return {"message": "User updated successfully"}

@router.delete("/{id}")
async def delete_user(id: str, db=Depends(get_database)):
    await user_model.delete_user(db, id)
    return {"message": "User deleted successfully"}
