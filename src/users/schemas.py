from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    login: str = Field(min_length=1, max_length=64)
    email: EmailStr
    password: str

    def set_name(self, new_name: str):
        self.name = new_name

    def set_email(self, new_email: EmailStr):
        self.email = new_email

    def set_password(self, new_password: str):
        self.password = new_password

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    login: str = Field(min_length=1, max_length=64)
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=128)
    email: EmailStr | None = None
    password: str | None = None
