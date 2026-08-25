from fastapi import APIRouter, HTTPException, Depends
from fastapi import status

from typing import Annotated

from src.users.dependecies import UserService, get_user_service
from src.users.schemas import User, UserCreate, UserUpdate

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/{user_id}")
def show_user(user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = user_service.show_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users_router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def add_user(user_data: UserCreate, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.add_user(user_data)

@users_router.patch("/{user_id}")
def change_user(
        user_id: int,
        user_service: Annotated[UserService, Depends(get_user_service)],
        user_data: UserUpdate) -> User:
    user = user_service.change_user(user_id, **user_data.model_dump())
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user