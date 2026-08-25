from abc import ABC, abstractmethod

from src.users.schemas import User

class UserStorage(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User | None:...

    @abstractmethod
    def add_user(self, user_data: dict):...

    @abstractmethod
    def delete_user(self, user_id: int) -> User | None:...

    @abstractmethod
    def change_user(self, user_id: int, **changes) -> User | None:...

class UserInMemoryStorage(UserStorage):
    def __init__(self):
        self.users: dict[int, User] = {}
        self.current_id = 0

    def get_user(self, user_id: int) -> User | None:
        return self.users.get(user_id)

users = UserInMemoryStorage()
