from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать задачу")],
        [KeyboardButton(text="Показать задачи")],
        [KeyboardButton(text="Поиск задачи")],
    ],
    resize_keyboard=True,
)


builder = InlineKeyboardBuilder()

choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отметить задачу выполненной", callback_data="markTaskDone"
            )
        ],
        [InlineKeyboardButton(text="Удалить задачу", callback_data="deleteTask")],
    ]
)

builder.attach(InlineKeyboardBuilder.from_markup(choice))
