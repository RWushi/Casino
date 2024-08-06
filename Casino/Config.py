from aiogram import BaseMiddleware
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from States import PostgresStateStorage
import asyncpg, json, os

wait = "⏳"

DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'rcasino',
    'user': 'postgres',
    'password': 's4kUp3Nc1rCl3s&',
    'port': '5432'
}

storage = PostgresStateStorage(**DATABASE_CONFIG)

async def create_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)

class DB:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


async def add_new_user(user_id):
    async with DB() as conn:
        await conn.execute('''
            INSERT INTO user_settings (user_id, language, demo_account, real_account, demo_bet, real_bet) 
            VALUES ($1, NULL, 10000, 0, 100, 100) ON CONFLICT (user_id) DO NOTHING
        ''', user_id)


class UserState(StatesGroup):
    language = State()
    menu = State()
    games = State()
    account = State()
    about = State()
    settings = State()
    slots = State()
    dice = State()

bot = Bot(token='7038676357:AAHFqmRyF1GbyL_zl47RBkT5MBxV7okcvrI')
dp = Dispatcher(bot, storage=storage)


TRANSLATIONS = {}

def load_translations():
    for lang_file in os.listdir("translations"):
        if lang_file.endswith(".json"):
            lang_code = lang_file[:-5]
            with open(f"translations/{lang_file}", "r", encoding="utf-8") as f:
                TRANSLATIONS[lang_code] = json.load(f)

load_translations()


def get_translation(language_code, category, key):
    value = TRANSLATIONS.get(language_code, {}).get(category, {}).get(key)
    return value

async def get_language(user_id):
    async with DB() as conn:
        chosen_lang = await conn.fetchval('SELECT language FROM user_settings WHERE user_id = $1', user_id)
    return chosen_lang

class LanguageMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        chat_id = message.chat.id
        message.conf['language_code'] = await get_language(chat_id)

dp.middleware.setup(LanguageMiddleware())
