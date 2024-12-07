import logging
import httpx

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.Sender.broadcast import CreateTaskState, FindTaskState 
from src.bot.Sender.utils import show_find_result, show_task_summary

from src.bot.config import FASTAPI_URL



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

    data = await state.get_data()
    task_name = data.get("task_name")
    description = data.get("description", None)
    date = data.get("date", None)

    await show_task_summary(message, state)
    await state.clear()


@router.message(F.text == "Поиск задачи")
async def start_searching(message: Message, state: FSMContext):
    logging.info("State started")
    await state.set_state(FindTaskState.task_id)
    await message.answer("Введите id задачи")


@router.message(FindTaskState.task_id)
async def find_task(message: Message, state: FSMContext):
    await state.update_data(task_id=int(message.text))
    await state.set_state(FindTaskState.confirmation)
    logging.info(f"(task_id): {message.text}")

    await show_find_result(message, state)


@router.callback_query(FindTaskState.confirmation, F.data == "markTaskDone")
async def mark_task(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')

    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"{FASTAPI_URL}operations/tasks/{task_id}")

            response_message = response.json()["Message"]

            await query.answer(response_message)
            await state.clear()

    except Exception as e:
        logging.error(f"Something wrong: {e}")
        await query.answer("Произошла ошибка")
        await state.clear()


@router.callback_query(FindTaskState.confirmation, F.data == "deleteTask")
async def delete_task(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{FASTAPI_URL}operations/tasks/{task_id}")

            response_message = response.json()["Message"]

            await query.answer(response_message)
            await state.clear()

    except Exception as e:
        logging.error(f"Something wrong: {e}")
        await query.answer("Произошла ошибка")
        await state.clear()
