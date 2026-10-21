from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("mysql+mysqldb://root:012356101007Az@localhost/task_tracker", echo=True)

class Base(DeclarativeBase):...
