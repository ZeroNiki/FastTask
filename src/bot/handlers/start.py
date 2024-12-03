from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    fullname = message.from_user.full_name
    await message.answer(f"Привет {html.bold(fullname)}! Я менеджер задач\nЧем могу помочь?")
