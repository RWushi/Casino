from aiogram.types import Message, CallbackQuery
from Config import bot, dp, UserState, DB, add_new_user, get_translation, wait
from Keyboards import language_kb
from HelloMessages import menu

async def language_start(chat_id):
    await bot.send_message(chat_id, "Choose your language / 选择你的语言 / Выберите язык / Тілді таңдаңыз:", reply_markup=language_kb)


@dp.message_handler(commands=['start'], state="*")
async def start(message: Message):
    user_id = message.from_user.id
    await add_new_user(user_id)
    await UserState.language.set()
    await language_start(user_id)

import Menu

async def language_finish(chat_id, language_code):
    text = get_translation(language_code, "Languages", "language_chosen")
    await bot.send_message(chat_id, text=text)
    await menu(chat_id)


@dp.callback_query_handler(lambda c: 'lang:' in c.data, state=UserState.language)
async def language_chosen(call: CallbackQuery):
    user_id = call.message.chat.id

    await bot.send_message(user_id, wait)

    language_code = call.data.split(":")[1]

    async with DB() as conn:
        await conn.execute('UPDATE user_settings SET language = $1 WHERE user_id = $2', language_code, user_id)

    await language_finish(user_id, language_code)


if __name__ == '__main__':
    dp.start_polling(skip_updates=True)