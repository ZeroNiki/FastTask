import logging
import httpx

from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from src.bot.config import FASTAPI_URL

from src.db import crud
from src.db.database import init_db, SessionLocal


router = Router()

init_db()

@router.message(CommandStart())
async def command_start(message: Message):
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    db = SessionLocal()
    try:
        crud.create_user(db, user_id, username)
        await message.answer(f"Привет {html.bold(fullname)}! Я менеджер задач\nЧем могу помочь?")
        logging.info(f"User {username} with id {user_id} created successfully.")
    except Exception as e:
        logging.error(f"Error while creating user: {e}")
        await message.reply("Извините, произошла ошибка при создании пользователя.")
    finally:
        db.close()
