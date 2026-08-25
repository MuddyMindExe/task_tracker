import json
from abc import ABC, abstractmethod

from src.users.schemas import User, UserCreate

class UserStorage(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> User | None:...

    @abstractmethod
    def add_user(self, user_data: UserCreate):...

    @abstractmethod
    def delete_user(self, user_id: int) -> User | None:...

    @abstractmethod
    def change_user(self, user_id: int, **changes) -> User | None:...

class UserJsonStorage(UserStorage):
    def __init__(self, file="src/storage/users.json"):
        self.file = file

    def get_user(self, user_id: int) -> User | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
        raw = data.get(str(user_id))
        return User.model_validate(raw) if raw else None

    def add_user(self, user_data: UserCreate) -> None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
            user_id = str(self.get_id())

        user = User(
            name=user_data.name,
            login=user_data.login,
            email=user_data.email,
            password=user_data.password
        )
        user = user.model_dump()
        data[user_id] = user
        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
        return user

    def delete_user(self, user_id: int) -> User | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)

        user = data.pop(str(user_id), None)

        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        return User.model_validate(user) if user else None

    def change_user(self, user_id: int, **changes) -> User | None:
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)

        user = User.model_validate(data.pop(str(user_id), None))
        if not user:
            return None
        for param, value in changes.items():
            if hasattr(user, param):
                if value is not None:
                    setattr(user, param, value)
        data[str(user_id)] = user.model_dump()

        with open(self.file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

        return user

    def get_id(self):
        with open(self.file, "r", encoding="utf-8") as file:
            data = json.load(file)
            return max(map(int, data.keys()), default=0) + 1
