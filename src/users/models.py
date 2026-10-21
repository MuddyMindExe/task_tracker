from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    login: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(256))
    password: Mapped[int]

    def __repr__(self):
        return (f"id: {self.id!r}\n"
                f"name: {self.name!r}\n"
                f"login: {self.login!r}\n"
                f"email: {self.email!r}\n"
                f"password: {self.password!r}")
