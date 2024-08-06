from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from Config import UserState, bot, dp
from aiogram import executor

async def language_start(chat_id):
    kb = dice_forecast_kb()
    await UserState.dice.set()
    await bot.send_message(chat_id, "ТЕСТ", reply_markup=kb)


@dp.message_handler(commands=['start'], state="*")
async def start(message: Message):
    user_id = message.from_user.id
    await language_start(user_id)


def dice_forecast_kb():
    kb = InlineKeyboardMarkup()

    button_1 = InlineKeyboardButton("·1·", callback_data="forecast:1")
    button_2 = InlineKeyboardButton("2", callback_data="forecast:2")

    kb.add(button_1, button_2)

    return kb


@dp.callback_query_handler(lambda c: 'forecast:' in c.data, state=UserState.dice)
async def forecast(call: CallbackQuery):
    user_id = call.message.chat.id

    chosen_forecast = call.data.split(":")[1]

    if chosen_forecast == "1":
        forecast = 1
        print(forecast)
        await bot.send_message(user_id, "Отклик пошел, кнопка 1 нажата")

    elif chosen_forecast == "2":
        forecast = 2
        print(forecast)
        await bot.send_message(user_id, "Отклик пошел, кнопка 2 нажата")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)