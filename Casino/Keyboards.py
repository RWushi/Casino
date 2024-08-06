from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from Config import get_translation

language_kb = InlineKeyboardMarkup()
english = InlineKeyboardButton("English🇺🇸", callback_data="lang:EN")
chinese = InlineKeyboardButton("中文🇨🇳", callback_data="lang:CN")
russian = InlineKeyboardButton("Русский🇷🇺", callback_data="lang:RU")
kazakh = InlineKeyboardButton("Қазақша🇰🇿", callback_data="lang:KZ")

language_kb.add(english, chinese)
language_kb.add(russian, kazakh)


def menu_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Menu", "games"))],
            [KeyboardButton(text=get_translation(language_code, "Menu", "account"))],
            [
                KeyboardButton(text=get_translation(language_code, "Menu", "about_bot")),
                KeyboardButton(text=get_translation(language_code, "Menu", "settings"))
            ],
            [KeyboardButton(text=get_translation(language_code, "Menu", "made_by_rtools"))]
        ],
        resize_keyboard=True
    )
    return kb

def games_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Games", "slots"))],
            [KeyboardButton(text=get_translation(language_code, "Games", "dice"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def account_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Account", "deposit"))],
            [KeyboardButton(text=get_translation(language_code, "Account", "top_up"))],
            [KeyboardButton(text=get_translation(language_code, "Account", "withdraw"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def about_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "About", "about_product"))],
            [
                KeyboardButton(text=get_translation(language_code, "About", "features")),
                KeyboardButton(text=get_translation(language_code, "About", "advantages"))
            ],
            [KeyboardButton(text=get_translation(language_code, "About", "fair_game"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def settings_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Settings", "my_id"))],
            [KeyboardButton(text=get_translation(language_code, "Settings", "change_language"))],
            [KeyboardButton(text=get_translation(language_code, "Settings", "support"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_menu"))]
        ],
        resize_keyboard=True
    )
    return kb

def slots_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Subcommon", "information"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb

def slots_bet_kb(language_code, demo_bet):
    kb = InlineKeyboardMarkup()
    min = InlineKeyboardButton(get_translation(language_code, "Betting", "min"), callback_data="bet:min")
    bet = InlineKeyboardButton(demo_bet, callback_data="bet:bet")
    max = InlineKeyboardButton(get_translation(language_code, "Betting", "max"), callback_data="bet:max")
    minus10 = InlineKeyboardButton("-10", callback_data="bet:-10")
    plus10 = InlineKeyboardButton("+10", callback_data="bet:+10")
    minus100 = InlineKeyboardButton("-100", callback_data="bet:-100")
    plus100 = InlineKeyboardButton("+100", callback_data="bet:+100")
    half = InlineKeyboardButton("÷2", callback_data="bet:/2")
    go = InlineKeyboardButton(get_translation(language_code, "Betting", "go"), callback_data="bet:go")
    double = InlineKeyboardButton("×2", callback_data="bet:*2")

    kb.add(min, bet, max)
    kb.add(minus10, plus10)
    kb.add(minus100, plus100)
    kb.add(half, go, double)

    return kb

def dice_kb(language_code):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_translation(language_code, "Subcommon", "information"))],
            [KeyboardButton(text=get_translation(language_code, "Common", "return_back"))]
        ],
        resize_keyboard=True
    )
    return kb

def dice_bet_kb(language_code, demo_bet):
    kb = InlineKeyboardMarkup()
    min = InlineKeyboardButton(get_translation(language_code, "Betting", "min"), callback_data="bet:min")
    bet = InlineKeyboardButton(demo_bet, callback_data="bet:bet")
    max = InlineKeyboardButton(get_translation(language_code, "Betting", "max"), callback_data="bet:max")
    minus10 = InlineKeyboardButton("-10", callback_data="bet:-10")
    plus10 = InlineKeyboardButton("+10", callback_data="bet:+10")
    minus100 = InlineKeyboardButton("-100", callback_data="bet:-100")
    plus100 = InlineKeyboardButton("+100", callback_data="bet:+100")
    half = InlineKeyboardButton("÷2", callback_data="bet:/2")
    double = InlineKeyboardButton("×2", callback_data="bet:*2")
    go = InlineKeyboardButton(get_translation(language_code, "Betting", "go"), callback_data="bet:go")
    forecast = InlineKeyboardButton(get_translation(language_code, "Betting", "forecast"), callback_data="bet:forecast")

    kb.add(min, bet, max)
    kb.add(minus10, plus10)
    kb.add(minus100, plus100)
    kb.add(half, double)
    kb.add(go, forecast)

    return kb

def dice_forecast_kb(language_code, demo_bet, forecast_list):
    kb = InlineKeyboardMarkup()

    if forecast_list is None:
        forecast_list = []

    button_1 = InlineKeyboardButton("·1·" if '1' in forecast_list else "1", callback_data="bet:1")
    button_2 = InlineKeyboardButton("·2·" if '2' in forecast_list else "2", callback_data="forecast:2")
    button_3 = InlineKeyboardButton("·3·" if '3' in forecast_list else "3", callback_data="forecast:3")
    button_4 = InlineKeyboardButton("·4·" if '4' in forecast_list else "4", callback_data="forecast:4")
    button_5 = InlineKeyboardButton("·5·" if '5' in forecast_list else "5", callback_data="forecast:5")
    button_6 = InlineKeyboardButton("·6·" if '6' in forecast_list else "6", callback_data="forecast:6")
    bet = InlineKeyboardButton(demo_bet, callback_data="forecast:bet")
    go = InlineKeyboardButton(get_translation(language_code, "Betting", "go"), callback_data="forecast:go")

    kb.add(button_1, button_2)
    kb.add(button_3, button_4)
    kb.add(button_5, button_6)
    kb.add(bet, go)

    return kb
