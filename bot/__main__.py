import logging
import asyncio
import sys

from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import User

from bot.handlers import user, admin
from bot.middlewares import DbSessionMiddleware

from config import BOT_TOKEN

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker
)


async def run():
    logging.basicConfig(level=logging.INFO)
    engine = create_async_engine(url='sqlite+aiosqlite:///dbase.db', echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        )
    )

    my_bot: User = await bot.get_me()
    if my_bot is None:
        logging.error("Bot tokeni orqali ulanib bo'lmayapti. Tokenni tekshirib ko'ring...")
        sys.exit(1)

    
    dp = Dispatcher()

    dp['dp'] = dp
    dp['bot'] = bot
    dp['ref_link'] = f"https://t.me/{my_bot.username}?start="

    mid = DbSessionMiddleware(session_pool=sessionmaker)
    dp.message.outer_middleware(mid)
    dp.callback_query.outer_middleware(mid)
    dp.include_router(admin.router)
    dp.include_router(user.router)
    
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(run())