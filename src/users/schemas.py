from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=128)
    login: str = Field(min_length=1, max_length=64)
    email: EmailStr
    hash_password: str

    def change_name(self, new_name: str):
        self.name = new_name

    def change_password(self, new_password: str):
        self.hash_password = new_password
