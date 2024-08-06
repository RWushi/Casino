from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Config import dp, UserState, get_translation, wait
from HelloMessages import games, account, about, settings
import Games, Account, About, Settings


@dp.message_handler(state=UserState.menu)
async def menu_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Menu", "games"):
        await message.answer(wait)
        await games(chat_id)

    elif message.text == get_translation(language_code, "Menu", "account"):
        await message.answer(wait)
        await account(chat_id)

    elif message.text == get_translation(language_code, "Menu", "about_bot"):
        await message.answer(wait)
        await about(chat_id)

    elif message.text == get_translation(language_code, "Menu", "settings"):
        await message.answer(wait)
        await settings(chat_id)

    elif message.text == get_translation(language_code, "Menu", "made_by_rtools"):
        button = InlineKeyboardButton(get_translation(language_code, "Menu", "contact"), url="https://t.me/wuxieten")
        kb = InlineKeyboardMarkup().add(button)
        await message.answer(get_translation(language_code, "Menu", "rtools"), reply_markup= kb)
