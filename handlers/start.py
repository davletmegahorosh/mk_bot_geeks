from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards.all_kbs import main_kb

start_router = Router()

@start_router.message(Command('start'))
async def start(message: types.Message):
    await message.answer('Здравствуйте, это бот для регисьрации и промотра аккаунта других пользователей.\n\n'
                         'пройдите регисьрацию нажав на кнопку ниже или если вы регистрировались, можете посмотреть дркгие профили',
                         reply_markup=await main_kb(message.from_user.id))