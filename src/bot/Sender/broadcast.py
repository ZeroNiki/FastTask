from aiogram.fsm.state import State, StatesGroup

class CreateTaskState(StatesGroup):
    task_name = State()
    description = State()


class FindTaskState(StatesGroup):
    task_id = State()
    confirmation = State()
