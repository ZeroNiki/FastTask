from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    user_id: int
    username: str


class TaskCreate(BaseModel):
    user_id: int
    task_name: str
    description: Optional[str] = None
    date: Optional[str] = None

    def set_default_date(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self
