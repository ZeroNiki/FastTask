import logging
import httpx
from aiogram import html
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from src.bot.config import FASTAPI_URL


async def show_task_summary(message: Message, state: FSMContext) -> None:
    task_data = await state.get_data()
    task_name = task_data.get("task_name")
    description = task_data.get("description")
    date = task_data.get("date")
    user_id = message.from_user.id

    try:
        async with httpx.AsyncClient() as client:
            payload = {
                    "user_id": user_id,
                    "task_name": task_name,
                    "description": description,
                    "date": date 
            }
            logging.info(f"Sending data to API: {payload}")
            response = await client.post(f"{FASTAPI_URL}operations/tasks", json=payload)


            if response.status_code == 200:
                data = response.json()
                task_msg = "\n\n".join([f"{html.bold('Название')}: {html.bold(data['task_name'])}\n"
                            f"{html.bold('Описание')}: {data['description']}\n"
                            f"{html.bold('Дата')}: {data['date']}\n"
                            f"{html.bold('Статус')}: {'Выполнено ✅' if data['is_done'] else 'Не выполнено ❌'}"])

                await message.answer(f"{task_msg}")
            else:
                await message.answer("Произошла ошибка!")
    except Exception as e:
        logging.error(f"Something wrong: {e}")
        await message.answer("Произошла ошибка!")



# TEST: Test this
async def show_find_result(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    task_id = data.get('task_id') 

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FASTAPI_URL}operations/find_task/{task_id}")
            data = response.json()

            if response.status_code == 200:
                task_msg = [f"🔹 {html.bold('ID')}: {data['id']}\n"
                            f"{html.bold('Название')}: {html.bold(data['task_name'])}\n"
                            f"{html.bold('Описание')}: {data['description']}\n"
                            f"{html.bold('Дата')}: {data['date']}\n"
                            f"{html.bold('Статус')}: {'Выполнено ✅' if data['is_done'] else 'Не выполнено ❌'}"]

                await message.answer(f"{task_msg}")


    except Exception as e:
        logging.error(f"Something wrong: {e}")
