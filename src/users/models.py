from sqlalchemy import Table, Column, String, Integer

from src.database import metadata_obj

# class Users(Base):
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(128))
#     login: Mapped[str] = mapped_column(String(64))
#     email: Mapped[str] = mapped_column(String(256))
#     password: Mapped[int]
#
#     def __repr__(self):
#         return (f"id: {self.id!r}\n"
#                 f"name: {self.name!r}\n"
#                 f"login: {self.login!r}\n"
#                 f"email: {self.email!r}\n"
#                 f"password: {self.password!r}")

users = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128)),
    Column("login", String(64)),
    Column("email", String(256)),
    Column("password", Integer)
)
