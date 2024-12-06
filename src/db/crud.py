from typing import Optional
from sqlalchemy.orm import Session

from src.db.models import User, Task
from src.db.schemas import TaskCreate

def create_user(db: Session, user_id: int, username: str):
    db_user = User(id=user_id, username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_task(db: Session, user_id: int, task_name: str, description: Optional[str] = None, date: Optional[str] = None):
    db_task = Task(user_id=user_id, task_name=task_name, description=description, date=date)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


def mark_task_done(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.is_done = True
        db.commit()
        db.refresh(db_task)
        return db_task

    return None


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise ValueError(f"Task with id {task_id} not found.")

    db.delete(db_task)
    db.commit()


def find_user_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise ValueError(f"Task with id {task_id} not found")

    return db_task
