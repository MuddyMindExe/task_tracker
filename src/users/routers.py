from fastapi import APIRouter, HTTPException

from src.users.service import user_service

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/{user_id}")
def show_user(user_id: int):
    user = user_service.show_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.post("/{user_id}")
def
