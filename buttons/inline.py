from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
import math

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Database.tables import Menu, Session


class Foot(CallbackData, prefix="foot"):
    id: int


class Paganate(CallbackData, prefix="paganate"):
    page: int


class Stock(CallbackData, prefix="stock"):
    foot_id: int
    quantity: int


class Add(CallbackData, prefix="add"):
    foot_id: int
    quantity: int


def basket_keyboard():
    button = [
        [InlineKeyboardButton(text="✅ Оформить заказ", callback_data="confirm_order")],
        [InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=button)


def basket_and_add_button():
    buttons = [[
        InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data="add_to_basket"),
        InlineKeyboardButton(text="🧺 Корзина", callback_data="basket")
    ]]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def add_to_basket(page, satr=9, ustun=3):
    with Session() as session:
        foots = session.query(Menu).all()

    buttons = foots[(page - 1) * satr:(page - 1) * satr + satr]
    builder = InlineKeyboardBuilder()
    for foot in buttons:
        builder.button(text=f"{foot.name[:10]}.." if len(foot.name) > 10 else foot.name,
                       callback_data=Foot(id=foot.id).pack())

    builder.adjust(ustun)

    menu_buttons = []

    if page > 1:
        menu_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=Paganate(page=page - 1).pack()))

    menu_buttons.append(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu"))

    if page < math.ceil(len(foots) / satr):
        menu_buttons.append(InlineKeyboardButton(text="➡️", callback_data=Paganate(page=page + 1).pack()))

    builder.row(*menu_buttons)

    return builder.as_markup()


def add(foot_id, quantity=1):
    builder = InlineKeyboardBuilder()
    if quantity > 1:
        builder.button(text="➖", callback_data=Stock(foot_id=foot_id, quantity=quantity - 1).pack())
    if quantity < 100:
        builder.button(text="➕", callback_data=Stock(foot_id=foot_id, quantity=quantity + 1).pack())

    builder.button(text="📥 В корзину", callback_data=Add(foot_id=foot_id, quantity=quantity).pack())

    builder.button(text="🔙 Назад в меню", callback_data="back_to_menu")
    builder.adjust(2)

    return builder.as_markup()
