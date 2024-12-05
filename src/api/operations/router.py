from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.database import init_db
from src.db.models import User, Task
from src.db.utils import get_db
from src.db.schemas import UserCreate, TaskCreate
from src.db import crud


init_db()


router = APIRouter(
        prefix="/operations",
        tags=["Operations"]
)


@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user.user_id).first()

    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(id=user.user_id, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
            "Message": "User create successfully", 
            "user": new_user
            }


@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task = task.set_default_date()

    try:
        task = crud.create_task(db, task.user_id, task.task_name, task.description, task.date)
        return {"task_name": task.task_name, "description": task.description, "date": task.date, "is_done": task.is_done}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error while creating task {e}")


@router.get("/tasks/{user_id}")
async def get_user_task(user_id: int, db: Session = Depends(get_db)):
    tasks = crud.get_user_tasks(db, user_id)
    return [{ "id": task.id, 
              "task_name": task.task_name, 
              "description": task.description, 
              "date": task.date, 
              "is_done": task.is_done } for task in tasks]


@router.patch("/tasks/{task_id}")
async def mark_task_done(task_id: int, db: Session = Depends(get_db)):
    task = crud.mark_task_done(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"Message": "Task marked as done", "task_id": task.id}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return {"Message": "Task delete successfully"}


@router.get("/tasks")
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [{ "id": task.id, 
              "task_name": task.task_name, 
              "description": task.description, 
              "date": task.date, 
              "is_done": task.is_done } for task in tasks]
