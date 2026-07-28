from src.users.schemas import User

class UserStorage:
    def __init__(self):
        self.users: dict[int, User] = {}
        self.current_id = 0

    def get_user(self, user_id: int) -> User | None:
        return self.users.get(user_id)
