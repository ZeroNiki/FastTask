import logging
import httpx
from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.bot.config import FASTAPI_URL


router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    fullname = message.from_user.full_name
    await message.answer(f"Привет {html.bold(fullname)}! Я менеджер задач\nЧем могу помочь?")


@router.message(Command("get_root"))
async def get_root(message: Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FASTAPI_URL)
            data = response.json()

            await message.reply(f"{data}")
    except Exception as e:
        logging.error(f"Error while fetching data from FastAPI: {e}")
        await message.reply("Извините, произошла ошибка при получении данных из FastAPI.")
