from sqlalchemy import Table, Column, String, Integer, Boolean, ForeignKey

from src.database import metadata_obj

# class Tasks(Base):
#     __tablename__ = "tasks"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(256))
#     description: Mapped[str] = mapped_column(String(256))
#     status: Mapped[bool]
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#
#     def __repr__(self):
#         return (f"id: {self.id!r}\n"
#                 f"title: {self.title!r}\n"
#                 f"desc: {self.description!r}\n"
#                 f"status: {self.status!r}\n"
#                 f"user_id: {self.user_id!r}")


tasks = Table(
    "tasks",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256), nullable=False),
    Column("description", String(256)),
    Column("status", Boolean),
    Column("user_id", Integer, ForeignKey("users.id"))
)