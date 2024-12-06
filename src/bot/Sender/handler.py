import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.bot.Sender.broadcast import CreateTaskState, FindTaskState 
from src.bot.Sender.utils import show_find_result, show_task_summary



router = Router()


@router.message(F.text == "Создать задачу")
async def start_broadcast(message: Message, state: FSMContext):
    logging.info("State started")
    await state.set_state(CreateTaskState.task_name)
    await message.answer("Введите название задачи")


@router.message(CreateTaskState.task_name)
async def process_task_name(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    logging.info(f"(task_name): {message.text}")
    await state.set_state(CreateTaskState.description)
    await message.answer("Напиши описание к задачи")


@router.message(CreateTaskState.description)
async def process_task_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    logging.info(f"(description): {message.text}")
    await state.set_state(CreateTaskState.date)
    await message.answer("Напиши дату к задачи")


@router.message(CreateTaskState.date)
async def process_task_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    logging.info(f"(date): {message.text}")
    await state.set_state(CreateTaskState.confirmation)

    data = await state.get_data()
    task_name = data.get("task_name")
    description = data.get("description", None)
    date = data.get("date", None)

    await show_task_summary(message, state)


# TODO: add find_by_id task