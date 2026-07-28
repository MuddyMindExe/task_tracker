from src.users.storage import UserStorage

class UserService:
    def __init__(self, user_storage: UserStorage):
        self.user_storage = user_storage

    def show_user(self, user_id: int):
        return self.user_storage.get_user(user_id)


user_service = UserService(UserStorage())
