from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# routers 
from .handlers.command import router as start_rt

# Other
from .config import TOKEN


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main() -> None:
    dp.include_router(start_rt)

    await dp.start_polling(bot)
