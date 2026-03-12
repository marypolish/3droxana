from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext

from ..db.mongodb import get_database
from ..models import users as user_model
from ..schemas import users as user_schema
from ..schemas.users import UserLogin

router = APIRouter(prefix="/api/users", tags=["Users"])

# Використовуємо sha256_crypt, щоб уникнути обмеження bcrypt у 72 байти
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


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
    # Знаходимо користувача за email
    user_raw = await user_model.get_user_by_email(db, login.email)
    if not user_raw:
        raise HTTPException(status_code=401, detail="Невірна пошта або пароль")

    stored_hash = user_raw.get("password")
    if not stored_hash or not verify_password(login.password, stored_hash):
        raise HTTPException(status_code=401, detail="Невірна пошта або пароль")

    # Серіалізуємо користувача перед віддачею (без пароля)
    user = user_model.serialize_user(user_raw)
    return {"message": "Успішний вхід", "user": user}


@router.post("/register", response_model=str)
async def register_user(user: user_schema.UserCreate, db=Depends(get_database)):
    # Перевірка, чи email вже існує
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач з таким email вже існує")

    user_data = user.dict()
    user_data["password"] = hash_password(user_data["password"])

    return await user_model.create_user(db, user_data)


@router.put("/{id}")
async def update_user(id: str, user: user_schema.UserUpdate, db=Depends(get_database)):
    await user_model.update_user(db, id, {k: v for k, v in user.dict().items() if v is not None})
    return {"message": "User updated successfully"}


@router.delete("/{id}")
async def delete_user(id: str, db=Depends(get_database)):
    await user_model.delete_user(db, id)
    return {"message": "User deleted successfully"}
