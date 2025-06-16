from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Salom, {html.bold(message.from_user.first_name)}")
