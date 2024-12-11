import logging
import httpx

from aiogram import Router, html, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.bot.config import FASTAPI_URL
from src.bot.handlers import keyboard as kb

from src.db import crud
from src.db.database import init_db, SessionLocal


router = Router()

init_db()


@router.message(CommandStart())
async def command_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Anonymous"
    fullname = message.from_user.full_name

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{FASTAPI_URL}operations/users",
                json={"user_id": user_id, "username": username},
            )

            if response.status_code == 200:
                data = response.json()
                logging.info(f"User created: {data}")
            elif response.status_code == 400:
                logging.warning(f"User already exist: {user_id} {username}")
            else:
                logging.error(
                    f"Unexpected response: {response.status_code} {response.json()}"
                )

    except Exception as e:
        logging.error(f"Error while creating user: {e}")
        await message.reply(
            "Извините, произошла ошибка при создании пользователя. (Пользователь уже существует)",
            reply_markup=kb.main,
        )
        return

    await message.answer(
        f"Привет, {html.bold(fullname)}! Я менеджер задач.\nЧем могу помочь?",
        reply_markup=kb.main,
    )


@router.message(F.text == "Показать задачи")
async def get_user_task(message: Message):
    user_id = message.from_user.id
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{FASTAPI_URL}operations/tasks/{user_id}")

            if response.status_code == 200:
                data = response.json()

                if not data:
                    await message.reply("У вас нету задач")
                else:
                    task_list = "\n\n".join(
                        [
                            f"🔹 {html.bold('ID')}: {task['id']}\n"
                            f"{html.bold('Название')}: {html.bold(task['task_name'])}\n"
                            f"{html.bold('Описание')}: {task['description']}\n"
                            f"{html.bold('Дата создания')}: {task['date']}\n"
                            f"{html.bold('Статус')}: {'Выполнено ✅' if task['is_done'] else 'Не выполнено ❌'}"
                            for task in data
                        ]
                    )

                    await message.reply(f"Ваши задачи:\n\n{task_list}")
            else:
                await message.reply(
                    "Не удалось получить список задач. Попробуйте позже."
                )
    except Exception as e:
        logging.error(f"Error while fetching tasks: {e}")
        await message.reply("Произошла ошибка при получении задач. Попробуйте позже.")
