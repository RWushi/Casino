from aiogram.types import Message, CallbackQuery
from Config import bot, dp, DB, UserState, get_translation, wait
from HelloMessages import games
from Keyboards import slots_bet_kb
from SlotsMath import spin


class CallDataSlots:
    def __init__(self):
        self.calls = {}

    async def set_call(self, chat_id, call):
        self.calls[chat_id] = call

    async def get_call(self, chat_id):
        return self.calls[chat_id]

user_call_data_slots = CallDataSlots()


async def new_bet(call, language_code, demo_bet, user_id):
    async with DB() as conn:
        await conn.execute("UPDATE user_settings SET demo_bet = $1 WHERE user_id = $2", demo_bet, user_id)
    kb = slots_bet_kb(language_code, str(demo_bet))
    await call.message.edit_reply_markup(reply_markup=kb)


@dp.message_handler(state=UserState.slots)
async def slots_handler(message: Message):
    language_code = message.conf.get('language_code')
    chat_id = message.chat.id
    user_id = message.from_user

    if message.text == get_translation(language_code, "Subcommon", "information"):
        await message.answer(get_translation(language_code, "Slots", "information"))

    elif message.text == get_translation(language_code, "Common", "return_back"):
        await message.answer(wait)
        await games(chat_id)

    elif message.text.replace('.', '', 1).replace(',', '', 1).isdigit():
        demo_bet = message.text.replace(',', '.')
        call = await user_call_data_slots.get_call(chat_id)
        await new_bet(call, language_code, demo_bet, user_id)
        await message.delete()
    else:
        await message.answer(get_translation(language_code, "Betting", "enter_number"))



@dp.callback_query_handler(lambda c: 'bet:' in c.data, state=UserState.slots)
async def betting(call: CallbackQuery):
    user_id = call.message.chat.id

    await user_call_data_slots.set_call(user_id, call)

    async with DB() as conn:
        language_code = await conn.fetchval(
            "SELECT language FROM user_settings WHERE user_id = $1", user_id)
        demo_account = await conn.fetchval(
            "SELECT demo_account FROM user_settings WHERE user_id = $1", user_id)
        demo_bet = await conn.fetchval(
            "SELECT demo_bet FROM user_settings WHERE user_id = $1", user_id)

    bet_mod = call.data.split(":")[1]

    if bet_mod == "min":
        demo_bet = 10
        await new_bet(call, language_code, demo_bet, user_id)

    elif bet_mod == "max":
        demo_bet = demo_account
        await new_bet(call, language_code, demo_bet, user_id)

    elif bet_mod == "-10":
        demo_bet -= 10
        if 10 <= demo_bet <= demo_account:
            await new_bet(call, language_code, demo_bet, user_id)
        elif demo_bet > demo_account:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "no_account"))
        elif demo_bet < 10:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "too_low"))

    elif bet_mod == "+10":
        demo_bet += 10
        if 10 <= demo_bet <= demo_account:
            await new_bet(call, language_code, demo_bet, user_id)
        elif demo_bet > demo_account:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "no_account"))
        elif demo_bet < 10:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "too_low"))

    elif bet_mod == "-100":
        demo_bet -= 100
        if 10 <= demo_bet <= demo_account:
            await new_bet(call, language_code, demo_bet, user_id)
        elif demo_bet > demo_account:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "no_account"))
        elif demo_bet < 10:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "too_low"))

    elif bet_mod == "+100":
        demo_bet += 100
        if 10 <= demo_bet <= demo_account:
            await new_bet(call, language_code, demo_bet, user_id)
        elif demo_bet > demo_account:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "no_account"))
        elif demo_bet < 10:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "too_low"))

    elif bet_mod == "/2":
        demo_bet /= 2
        if 10 <= demo_bet <= demo_account:
            await new_bet(call, language_code, demo_bet, user_id)
        elif demo_bet > demo_account:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "no_account"))
        elif demo_bet < 10:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "too_low"))

    elif bet_mod == "*2":
        demo_bet *= 2
        if 10 <= demo_bet <= demo_account:
            await new_bet(call, language_code, demo_bet, user_id)
        elif demo_bet > demo_account:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "no_account"))
        elif demo_bet < 10:
            await bot.send_message(user_id, get_translation(language_code, "Betting", "too_low"))

    elif bet_mod == "go":
        await spin(user_id, demo_bet, language_code)