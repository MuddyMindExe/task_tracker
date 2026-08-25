from src.users.storage import UserStorage
from src.users.schemas import User, UserCreate, UserUpdate

class UserService:
    def __init__(self, user_storage: UserStorage):
        self.user_storage = user_storage

    def show_user(self, user_id: int) -> User | None:
        return self.user_storage.get_user(user_id)

    def add_user(self, user_data: UserCreate) -> User | None:
        return self.user_storage.add_user(user_data)

    def delete_user(self, user_id: int) -> User | None:
        return self.user_storage.delete_user(user_id)

    def change_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        return self.user_storage.change_user(user_id, **user_data.model_dump())
