from aiogram.types import CallbackQuery
from Config import bot, dp, DB, UserState
from HelloMessages import dice_bet_edit
from Keyboards import dice_forecast_kb
from DiceMath import throw


async def new_forecast(call, language_code, demo_bet, user_id, forecast):
    async with DB() as conn:
        await conn.execute("UPDATE user_settings SET dice_forecast = array_append(dice_forecast, $1) WHERE user_id = $2", forecast, user_id)
    kb = dice_forecast_kb(language_code, str(demo_bet), forecast)
    await call.message.edit_reply_markup(reply_markup=kb)


@dp.callback_query_handler(lambda c: 'forecast:' in c.data, state=UserState.dice)
async def forecast(call: CallbackQuery):
    user_id = call.message.chat.id

    async with DB() as conn:
        language_code = await conn.fetchval(
            "SELECT language FROM user_settings WHERE user_id = $1", user_id)
        demo_bet = await conn.fetchval(
            "SELECT demo_bet FROM user_settings WHERE user_id = $1", user_id)

    chosen_forecast = call.data.split(":")[1]

    if chosen_forecast == "1":
        forecast = 1
        await bot.send_message(user_id, "Отклик пошел, кнопка 1 нажата")
        await new_forecast(call, language_code, demo_bet, user_id, forecast)

    elif chosen_forecast == "2":
        forecast = 2
        await bot.send_message(user_id, "Отклик пошел, кнопка 2 нажата")
        await new_forecast(call, language_code, demo_bet, user_id, forecast)

    elif chosen_forecast == "3":
        forecast = 3
        await new_forecast(call, language_code, demo_bet, user_id, forecast)

    elif chosen_forecast == "4":
        forecast = 4
        await new_forecast(call, language_code, demo_bet, user_id, forecast)

    elif chosen_forecast == "5":
        forecast = 5
        await new_forecast(call, language_code, demo_bet, user_id, forecast)

    elif chosen_forecast == "6":
        forecast = 6
        await new_forecast(call, language_code, demo_bet, user_id, forecast)

    elif chosen_forecast == "bet":
        await dice_bet_edit(user_id, language_code)

    elif chosen_forecast == "go":
        await throw(user_id, demo_bet, language_code)