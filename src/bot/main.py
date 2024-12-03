from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# routers 
from .handlers.start import router as start_rt

# Other
from .config import TOKEN


dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def main() -> None:
    dp.include_router(start_rt)

    await dp.start_polling(bot)


async def stop_bot():
    try:
        if dp._polling:
            await dp.stop_polling()

        await bot.session.close()
        await dp.storage.close()
        print("Bot stopped successfully.")
    except Exception as e:
        print(f"Error stopping bot: {e}")

