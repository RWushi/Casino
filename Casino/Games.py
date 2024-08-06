from aiogram.types import Message
from Config import dp, UserState, get_translation, wait
from HelloMessages import slots, dice, menu
import Slots, Dice

@dp.message_handler(state=UserState.games)
async def about_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id

    if message.text == get_translation(language_code, "Games", "slots"):
        await message.answer(wait)
        await slots(chat_id)

    if message.text == get_translation(language_code, "Games", "dice"):
        await message.answer(wait)
        await dice(chat_id)

    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(chat_id)
