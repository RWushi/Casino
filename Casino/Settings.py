from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Config import dp, bot, UserState, DB, get_translation, wait
from HelloMessages import menu
from Keyboards import language_kb


@dp.message_handler(state=UserState.settings)
async def settings_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Settings", "my_id"):
        await message.answer(wait)
        await message.answer(f"{get_translation(language_code, 'Settings', 'your_id')}{message.from_user.id}\n{get_translation(language_code, 'Settings', 'id_info')}")


    elif message.text == get_translation(language_code, "Settings", "change_language"):
        await message.answer(get_translation(language_code, "Settings", "choose_language"), reply_markup=language_kb)

    elif message.text == get_translation(language_code, "Settings", "support"):
        button = InlineKeyboardButton(get_translation(language_code, "Settings", "contact"), url="https://t.me/RWushi")
        kb = InlineKeyboardMarkup().add(button)
        await message.answer(get_translation(language_code, "Settings", "contact_text"), reply_markup= kb)

    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(chat_id)


@dp.callback_query_handler(lambda c: 'lang:' in c.data, state=UserState.settings)
async def language_chosen(call: CallbackQuery):
    user_id = call.message.chat.id

    await bot.send_message(user_id, wait)

    language_code = call.data.split(":")[1]

    async with DB() as conn:
        await conn.execute('UPDATE user_settings SET language = $1 WHERE user_id = $2', language_code, user_id)

    await bot.send_message(user_id, get_translation(language_code, "Settings", "language_changed"))