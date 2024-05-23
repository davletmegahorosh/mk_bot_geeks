from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import database

async def gender_kb():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Мужской'),
             KeyboardButton(text='Женский'),
             KeyboardButton(text='Секрет')]
        ],
        resize_keyboard=True
    )
    return kb

async def main_kb(tg_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Смотреть анкеты', callback_data='view_ankets')]
        ])
    if database.is_exists(tg_id):
        return kb
    else:
        kb.inline_keyboard[0][0] = InlineKeyboardButton(text='Зрегистрироватся', callback_data='register')
        return kb


async def view_kb(tg_id):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='👍🏻', callback_data=f'like_{tg_id}'),
             InlineKeyboardButton(text='👎🏻', callback_data=f'dislike_{tg_id}'),
             InlineKeyboardButton(text='❌', callback_data='stop')]
        ]
    )
    return kb