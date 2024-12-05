from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Создать задачу")],
              [KeyboardButton(text="Получить задачу пользователя")],
              [KeyboardButton(text="Получить все задачи")]], resize_keyboard=True)


builder = InlineKeyboardBuilder()

chBtn = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отметить задачу выполненной", callback_data="markTaskDone")],
    [InlineKeyboardButton(text="Удалить задачу", callback_data="deleteTask")],
])

builder.attach(InlineKeyboardBuilder.from_markup(chBtn))
