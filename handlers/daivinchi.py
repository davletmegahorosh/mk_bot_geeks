from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import database, bot
from keyboards import all_kbs
from daivinchi_txt import anketa_text

daivinchi_router = Router()


class Anketa(StatesGroup):
    nickname = State()
    age = State()
    gender = State()
    extra_text = State()
    photo = State()


@daivinchi_router.callback_query(F.data == 'register')
async def start_comment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Как тебя зовут?👀')
    await callback.message.delete()
    await state.set_state(Anketa.nickname)


@daivinchi_router.message(Anketa.nickname)
async def load_nickname(message: types.Message, state: FSMContext):
    await state.update_data(tg_id=message.from_user.id)
    await state.update_data(nickname=message.text)
    await message.answer('Сколько тебе лет?')
    await state.set_state(Anketa.age)


@daivinchi_router.message(Anketa.age)
async def load_age(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 7 < int(message.text) < 70:
            await state.update_data(age=int(message.text))
            await message.answer('Какого ты пола', reply_markup=await all_kbs.gender_kb())
            await state.set_state(Anketa.gender)
        else:
            await message.answer('Введите свой настоящий возраст')
    else:
        await message.answer('Пишите только числа')


@daivinchi_router.message(Anketa.gender)
async def load_gender(message: types.Message, state: FSMContext):
    if message.text.lower() in ['мужской', 'женский', 'секрет']:
        await state.update_data(gender=message.text)
        await message.answer('Напишите небольшой текст про себя', reply_markup=all_kbs.ReplyKeyboardRemove())
        await state.set_state(Anketa.extra_text)
    else:
        await message.answer('Выберите из списка')

@daivinchi_router.message(Anketa.extra_text)
async def load_extra(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data(extra_text=message.text)
        await message.answer('Отправьте фото')
        await state.set_state(Anketa.photo)
    else:
        await message.answer('Напишите текст')




@daivinchi_router.message(Anketa.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        data = await state.get_data()
        text = await anketa_text(data['nickname'], data['age'], data['gender'], data['extra_text'])
        await message.answer_photo(data['photo'], caption=text)
        await message.answer('Вот ваша анкета. Вы успешно прошли регистрацию')
        database.insert_anketa(data)
        await state.clear()
        await message.answer('теперь вы можете посмотреть на профили тех кто тоже прошел регистрацию',
                             reply_markup=await all_kbs.main_kb(message.from_user.id))
    else:
        await message.answer('Отправьте фото')


# @daivinchi_router.message(Comments.extra_comment)
# async def load_extra_comment(message: types.Message, state: FSMContext):
#     await state.update_data(extra_comment=message.text)
#     data = await state.get_data()
#     print("~", data)
#     await message.answer('спасибо за отзыв\nвсего доброго')
#     await state.clear()
