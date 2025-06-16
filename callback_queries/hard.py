from aiogram import F, Router
from aiogram.types import CallbackQuery

from buttons.inline import Paganate, Foot, Stock, add_to_basket, add, Add

from Database.tables import Menu, Basket, Session

router = Router()

@router.callback_query(Foot.filter())
async def foot(callback_query: CallbackQuery, callback_data: Foot):
    with Session() as session:
        menu = session.query(Menu).filter(Menu.id == callback_data.id).first()

    res = f"{str(menu)}\n\n Количество: 1"

    await callback_query.message.edit_text(res, reply_markup=add(menu.id))

@router.callback_query(Paganate.filter())
async def paganate(callback_query: CallbackQuery, callback_data: Paganate):
    await callback_query.message.edit_text("📋 Выберите заказ:", reply_markup=add_to_basket(page=callback_data.page))

@router.callback_query(Stock.filter())
async def stock(callback_query: CallbackQuery, callback_data: Stock):
    with Session() as session:
        menu = session.query(Menu).filter(Menu.id == callback_data.foot_id).first()

    res = f"{f"<b>🏷️ {menu.name}</b>\n💰 Цена: <b>{menu.price*callback_data.quantity:,.2f}$</b>"}\n\n Количество: {callback_data.quantity}"

    await callback_query.message.edit_text(res, reply_markup=add(menu.id, quantity=callback_data.quantity))

@router.callback_query(Add.filter())
async def add_(callback_query: CallbackQuery, callback_data: Add):
    basket = Basket(user_id=callback_query.message.chat.id, foot_id=callback_data.foot_id, stock=callback_data.quantity)
    basket.add()
    await callback_query.message.edit_text("📋 Выберите заказ:", reply_markup=add_to_basket(page=1))
