from Config import bot, DB, get_translation
from HelloMessages import user_message_data, dice_bet
import asyncio, decimal


async def get_ratio(filtered_result, bet_type, forecast):
    if bet_type == "number":
        if filtered_result == forecast:
            return 5
        else:
            return -1
    elif bet_type == "parity":
        if (forecast == "even" and filtered_result % 2 == 0) or (forecast == "odd" and filtered_result % 2 != 0):
            return 1.8
        else:
            return -1
    elif bet_type == "range":
        if (forecast == "1-2" and filtered_result in [1, 2]) or \
                (forecast == "3-4" and filtered_result in [3, 4]) or \
                (forecast == "5-6" and filtered_result in [5, 6]):
            return 2.7
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


async def throw(user_id, demo_bet, language_code):
    message_id = await user_message_data.get_message_id(user_id)
    await bot.delete_message(user_id, message_id)

    result_dice = await bot.send_dice(user_id, emoji='🎲')
    filtered_result = result_dice.dice.value
    print (filtered_result)

    ratio = await get_ratio(filtered_result)

    result = await bet_result(ratio, demo_bet, user_id)

    if ratio > 0:
        result_message = (f"{get_translation(language_code, 'Subcommon', 'win_message')}{result}")
    else:
        result_message = get_translation(language_code, "Subcommon", "lose_message")

    await asyncio.sleep(3)
    await bot.send_message(user_id, result_message)
    await dice_bet(user_id, language_code)
