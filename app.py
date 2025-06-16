import asyncio
import logging
import sys
from os import getenv

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import *
from callback_queries import *

load_dotenv('.env')
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
async def main() -> None:
    dp.include_routers(start_router, menu_router, default_callback_router, hard_callback_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")