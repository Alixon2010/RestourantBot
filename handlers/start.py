from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from Database.tables import User, Session
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    if not User.exists(message.chat.id):
        with Session() as session:
            session.add(User(chat_id=message.chat.id, full_name=message.from_user.full_name))
            session.commit()

    await message.answer(f"👋 Привет, {html.bold(message.from_user.first_name)}\nДобро пожаловать в кафе! Чтобы открыть меню нажмите /menu")


