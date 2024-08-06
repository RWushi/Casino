from aiogram.types import Message
from Config import dp, DB, UserState, get_translation, wait
from HelloMessages import menu


@dp.message_handler(state=UserState.account)
async def menu_handler(message: Message):
    language_code = message.conf.get('language_code')
    user_id = message.from_user.id

    if message.text == get_translation(language_code, "Account", "deposit"):
        async with DB() as conn:
            demo_account = await conn.fetchval("SELECT demo_account FROM user_settings WHERE user_id = $1", user_id)
            real_account = await conn.fetchval("SELECT real_account FROM user_settings WHERE user_id = $1", user_id)
        await message.answer(f"{get_translation(language_code, 'Account', 'demo')}{demo_account}\n{get_translation(language_code, 'Account', 'real')}{real_account}")


    elif message.text == get_translation(language_code, "Account", "top_up"):
        await message.answer(get_translation(language_code, "Subcommon", "not_ready"))

    elif message.text == get_translation(language_code, "Account", "withdraw"):
        await message.answer(get_translation(language_code, "Subcommon", "not_ready"))

    elif message.text == get_translation(language_code, "Common", "return_menu"):
        await message.answer(wait)
        await menu(user_id)