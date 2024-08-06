from Config import bot, DB, UserState, get_language, get_translation
from Keyboards import menu_kb, games_kb, account_kb, about_kb, settings_kb, slots_kb, slots_bet_kb, dice_kb, dice_bet_kb, dice_forecast_kb


async def menu(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Menu", "menu")
    kb = menu_kb(language_code)
    await UserState.menu.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def games(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Games", "games")
    kb = games_kb(language_code)
    await UserState.games.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def account(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Account", "account")
    kb = account_kb(language_code)
    await UserState.account.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def about(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "About", "about")
    kb = about_kb(language_code)
    await UserState.about.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def settings(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Settings", "settings")
    kb = settings_kb(language_code)
    await UserState.settings.set()
    await bot.send_message(chat_id, text, reply_markup=kb)

async def slots(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Slots", "slots")
    kb = slots_kb(language_code)
    await UserState.slots.set()
    await bot.send_message(chat_id, text, reply_markup=kb)
    await slots_bet(chat_id, language_code)

async def slots_bet(chat_id, language_code):
    text = get_translation(language_code, "Slots", "bet")
    user_id = chat_id
    async with DB() as conn:
        demo_bet = await conn.fetchval("SELECT demo_bet FROM user_settings WHERE user_id = $1", user_id)
    kb = slots_bet_kb(language_code, str(demo_bet))
    message = await bot.send_message(chat_id, text, reply_markup=kb)
    message_id = message.message_id
    await user_message_data.set_message_id(user_id, message_id)

async def dice(chat_id):
    language_code = await get_language(chat_id)
    text = get_translation(language_code, "Dice", "dice")
    kb = dice_kb(language_code)
    await UserState.dice.set()
    await bot.send_message(chat_id, text, reply_markup=kb)
    await dice_bet(chat_id, language_code)

async def dice_bet(chat_id, language_code):
    text = get_translation(language_code, "Dice", "bet")
    user_id = chat_id
    async with DB() as conn:
        demo_bet = await conn.fetchval("SELECT demo_bet FROM user_settings WHERE user_id = $1", user_id)
    kb = dice_bet_kb(language_code, str(demo_bet))
    message = await bot.send_message(chat_id, text, reply_markup=kb)
    message_id = message.message_id
    await user_message_data.set_message_id(user_id, message_id)

async def dice_forecast(chat_id, language_code):
    text = get_translation(language_code, "Dice", "forecast")
    user_id = chat_id
    async with DB() as conn:
        demo_bet = await conn.fetchval("SELECT demo_bet FROM user_settings WHERE user_id = $1", user_id)
        forecast_list = await conn.fetchval("SELECT dice_forecast FROM user_settings WHERE user_id = $1", user_id)
    kb = dice_forecast_kb(language_code, str(demo_bet), forecast_list)
    message_id1 = await user_message_data.get_message_id(user_id)
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id1, text=text)
    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id1, reply_markup=kb)


async def dice_bet(chat_id, language_code):
    text = get_translation(language_code, "Dice", "bet")
    user_id = chat_id
    async with DB() as conn:
        demo_bet = await conn.fetchval("SELECT demo_bet FROM user_settings WHERE user_id = $1", user_id)
    kb = dice_bet_kb(language_code, str(demo_bet))
    message = await bot.send_message(chat_id, text, reply_markup=kb)
    message_id = message.message_id
    await user_message_data.set_message_id(user_id, message_id)


class MessageData:
    def __init__(self):
        self.messages = {}

    async def set_message_id(self, chat_id, message_id):
        self.messages[chat_id] = message_id

    async def get_message_id(self, chat_id):
        return self.messages.get(chat_id)

user_message_data = MessageData()