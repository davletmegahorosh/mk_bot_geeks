from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards.all_kbs import main_kb, view_kb
from config import database, bot
from random import choice
from daivinchi_txt import anketa_text

view_router = Router()

@view_router.callback_query(F.data == 'view_ankets')
async def view_ankets(call: types.CallbackQuery):
    ankets = database.select_ankets(call.from_user.id)
    print(ankets)
    if not ankets:
        if len(database.is_any_exists()) <= 1:
            await call.message.answer('Анкет пока что нету или вы уже все посмотрели.'
                                      ' Можете посмотреть те же анкеты снова',
                                      reply_markup=await main_kb(call.from_user.id))
            database.delete_my_like(call.from_user.id)
            await view_ankets(call)
        else:
            await call.message.answer('Анкет пока что нет.',reply_markup=await main_kb(call.from_user.id))

        await call.message.delete()
    else:
        chosen_anket = choice(ankets)
        text =await anketa_text(chosen_anket[2], chosen_anket[3], chosen_anket[4], chosen_anket[5])
        print(text)
        await call.message.answer_photo(photo=chosen_anket[6], caption=text, reply_markup=await view_kb(chosen_anket[1]))
        await call.message.delete()
        print(chosen_anket)


@view_router.callback_query(F.data.startswith('like_'))
@view_router.callback_query(F.data.startswith('dislike_'))
async def like(call: types.CallbackQuery):
    owner = int(call.data.replace("like_","").replace('dis',''))
    liker = call.from_user.id
    liker_name = call.from_user.full_name
    status = 1 if call.data.startswith('like_') else 0
    database.insert_like(liker, owner, status)
    if call.data.startswith('like_'):
        try:
            await bot.send_message(
                chat_id=owner,
                text=f"<a href='tg://user?id={liker}'>{liker_name}</a> лайкнул вашу анкету.",
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
    await view_ankets(call)

@view_router.callback_query(F.data == 'stop')
async def stop(call: types.CallbackQuery):
    await call.message.answer('просмотр анкет приостановлен. но вы сможете нажать на кнопку и продожить просмотр',
                              reply_markup=await main_kb(call.from_user.id))
    await call.message.delete()

