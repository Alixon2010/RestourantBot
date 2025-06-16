from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from buttons.inline import add_to_basket as button, basket_keyboard, basket_and_add_button
from buttons.keyboard import location

from aiogram.fsm.state import State, StatesGroup

from sqlalchemy import text
from Database.tables import Session, Basket, Menu

from dotenv import load_dotenv
from os import getenv

load_dotenv()


from app import bot
router = Router()

class GetLocation(StatesGroup):
    get_location = State()
    write = State()


@router.callback_query(F.data == "clear")
async def clear_callback(call: CallbackQuery):
    with Session() as session:
        session.query(Basket).filter(Basket.user_id == call.message.chat.id).delete()
        session.commit()

    with Session() as session:
        items = session.query(Menu).all()

    st = "🍽 Меню:\n\n"
    for index, item in enumerate(items, 1):
        st += f"{index}. <b>{item.name}</b> - {item.price}$\n"

    await call.message.edit_text(st, reply_markup=basket_and_add_button())

@router.callback_query(F.data == "add_to_basket")
async def add_to_basket(call: CallbackQuery):
    await call.message.edit_text("📋 Выберите заказ:", reply_markup=button(page=1))
    await call.answer()

@router.callback_query(F.data == "basket")
async def basket(call: CallbackQuery):
    with Session() as session:
        res = session.execute(text(f"""
        SELECT m.name, SUM(m.price * b.stock), SUM(b.stock) FROM basket b JOIN menu m ON b.foot_id = m.id WHERE b.user_id = {call.message.chat.id} GROUP BY b.foot_id, m.name""")).all()

        bask = ""
        summa = 0
        for index, item in enumerate(res, 1):
            bask += f"{index}. {item[0]} {item[2]}шт - {item[1]}$\n"
            summa += item[1]

    await call.message.edit_text(f"🧺 Ваша корзина:\n\n{bask}\n💰 Итого: {summa}$", reply_markup=basket_keyboard())
    await call.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(call: CallbackQuery):
    with Session() as session:
        items = session.query(Menu).all()

    st = "🍽 Меню:\n\n"
    for index, item in enumerate(items, 1):
        st += f"{index}. <b>{item.name}</b> - {item.price}$\n"

    await call.message.edit_text(st, reply_markup=basket_and_add_button())

@router.callback_query(F.data == "confirm_order")
async def confirm_order(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("📦 Как вы хотите указать адрес доставки?", reply_markup=location())
    await call.message.delete()
    await state.set_state(GetLocation.get_location)

@router.message(GetLocation.get_location)
async def get_location(message: Message, state: FSMContext):
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude

        with Session() as session:
            bask = session.execute(text(f"""
            SELECT m.name, SUM(m.price * b.stock), SUM(b.stock) FROM basket b JOIN menu m ON b.foot_id = m.id WHERE b.user_id = {message.chat.id} GROUP BY b.foot_id, m.name""")).all()

            res = f"👤 Заказшик: <b>{message.from_user.full_name}</b>\n\n"
            summa = 0
            for index, item in enumerate(bask, 1):
                res += f"{index}. <b>{item[0]}</b> {item[2]}шт - {item[1]}$\n"
                summa += item[1]

        res += f"\n📍 Локация: <code>{lat}</code> - <code>{lon}</code>\n💰 Итого: <b>{summa}$</b>"

        await state.clear()
        await message.answer("🕔 Заказ отправлен")
        await bot.send_message(chat_id=getenv("ADMIN"), text=res)

    if message.text == "✍️ Ввести вручную":
        await message.answer("✍️ Введите аддрес", reply_markup=ReplyKeyboardRemove())
        await state.set_state(GetLocation.write)

@router.message(GetLocation.write)
async def write(message: Message, state: FSMContext):
    with Session() as session:
        bask = session.execute(text(f"""
        SELECT m.name, SUM(m.price * b.stock), SUM(b.stock) FROM basket b JOIN menu m ON b.foot_id = m.id WHERE b.user_id = {message.chat.id} GROUP BY b.foot_id, m.name""")).all()

        res = f"👤 Заказшик: <b>{message.from_user.full_name}</b>\n\n"
        summa = 0
        for index, item in enumerate(bask, 1):
            res += f"{index}. <b>{item[0]}</b> {item[2]}шт - {item[1]}$\n"
            summa += item[1]


    res += f"\n📍 Локация: <b>{message.text}</b>\n💰 Итого: <b>{summa}$</b>"

    await state.clear()
    with Session() as session:
        session.query(Basket).filter(Basket.user_id == message.chat.id).delete()
        session.commit()
    await bot.send_message(chat_id=getenv("ADMIN"), text=res)
    await message.answer("🕔 Заказ отправлен")
    await state.clear()
