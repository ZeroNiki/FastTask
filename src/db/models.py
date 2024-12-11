from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from src.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_name = Column(String, index=True)
    description = Column(String)
    date = Column(String)
    is_done = Column(Boolean, default=False)
