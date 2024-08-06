from Config import bot, DB, get_translation
from HelloMessages import user_message_data, slots_bet
import asyncio, decimal

async def get_ratio(filtered_result):
    if filtered_result in (2, 3, 4, 5, 9, 13, 17, 33, 49):  # 2 бара
        return 0.25
    elif filtered_result in (11, 27, 35, 39, 41, 42, 44, 47, 59):  # 2 лимона
        return 0.25
    elif filtered_result in (6, 18, 21, 23, 24, 26, 30, 38, 54):  # 2 винограда
        return 0.5
    elif filtered_result in (16, 32, 48, 52, 56, 60, 61, 62, 63):  # 2 семерки
        return 1
    elif filtered_result == 1:  # 3 бара
        return 3
    elif filtered_result == 43:  # 3 лимона
        return 5
    elif filtered_result == 22:  # 3 винограда
        return 10
    elif filtered_result == 64:  # 3 семерки
        return 20
    else:
        return -1


async def bet_result(ratio, demo_bet, user_id):
    ratio_decimal = decimal.Decimal(str(ratio))
    result = demo_bet * ratio_decimal
    async with DB() as conn:
        demo_account = await conn.fetchval("SELECT demo_account FROM user_settings WHERE user_id = $1", user_id)
        demo_account = demo_account + result
        await conn.execute("UPDATE user_settings SET demo_account = $1 WHERE user_id = $2", demo_account, user_id)
    return result


async def spin(user_id, demo_bet, language_code):
    message_id = await user_message_data.get_message_id(user_id)
    await bot.delete_message(user_id, message_id)

    result_dice = await bot.send_dice(user_id, emoji='🎰')
    filtered_result = result_dice.dice.value

    ratio = await get_ratio(filtered_result)

    result = await bet_result(ratio, demo_bet, user_id)

    if ratio > 0:
        result_message = (f"{get_translation(language_code, 'Subcommon', 'win_message')}{result}")
    else:
        result_message = get_translation(language_code, "Subcommon", "lose_message")

    await asyncio.sleep(3)
    await bot.send_message(user_id, result_message)
    await slots_bet(user_id, language_code)

