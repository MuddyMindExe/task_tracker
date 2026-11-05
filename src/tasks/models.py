from sqlalchemy import Table, Column, String, Integer, Boolean, ForeignKey

from src.database import metadata_obj

tasks = Table(
    "tasks",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256), nullable=False),
    Column("description", String(256)),
    Column("status", Boolean),
    Column("user_id", Integer, ForeignKey("users.id"))
)
