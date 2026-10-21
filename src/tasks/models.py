from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256))
    status: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return (f"id: {self.id!r}\n"
                f"title: {self.title!r}\n"
                f"desc: {self.description!r}\n"
                f"status: {self.status!r}\n"
                f"user_id: {self.user_id!r}")
