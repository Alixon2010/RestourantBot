from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from Database.tables import Menu, Session, User

from buttons.inline import basket_and_add_button
router = Router()

@router.message(Command('menu'))
async def menu(message: Message):
    with Session() as session:
        items = session.query(Menu).all()

    if not User.exists(message.chat.id):
        with Session() as session:
            session.add(User(chat_id=message.chat.id, full_name=message.from_user.full_name))
            session.commit()
    st = "🍽 Меню:\n\n"
    for index, item in enumerate(items, 1):
        st+=f"{index}. <b>{item.name}</b> - {item.price}$\n"

    await message.answer(st, reply_markup=basket_and_add_button())