import logging
import httpx
from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.bot.config import FASTAPI_URL

from src.bot.db.task_manager import TasksDB


router = Router()

db = TasksDB()


@router.message(CommandStart())
async def command_start(message: Message):
    fullname = message.from_user.full_name
    tg_id = message.from_user.id
    username = message.from_user.username

    db.add_user(tg_id, username)

    await message.answer(f"Привет {html.bold(fullname)}! Я менеджер задач\nЧем могу помочь?")


@router.message(Command("get_root"))
async def get_root(message: Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FASTAPI_URL)
            data = response.json()["Message"]

            await message.reply(f"{data}")
    except Exception as e:
        logging.error(f"Error while fetching data from FastAPI: {e}")
        await message.reply("Извините, произошла ошибка при получении данных из FastAPI.")
