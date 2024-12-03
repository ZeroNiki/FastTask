import asyncio
import uvicorn
import logging
from fastapi import FastAPI

from src.bot.main import main as run_bot

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def startFastapi():
    logger.info("Starting FastAPI server...")
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8080)


async def startBot():
    logger.info("Starting aiogram bot...")
    await run_bot()


async def main():
    logger.info("Starting FastAPI and Aiogram...")
    loop = asyncio.get_event_loop()

    fastapi_task = loop.run_in_executor(None, startFastapi)
    bot_task = asyncio.create_task(startBot())

    await fastapi_task
    await bot_task


if __name__ == "__main__":
    logging.info("Application is starting...")
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occured: {e}")
