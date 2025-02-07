from typing import Callable, Awaitable, Dict, Any
from datetime import datetime

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

from bot.db.models import User, Admin


# SQLAlchemy connection'ni router'larga uzatadigan middleware
class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session

            user: User = (await session.execute(
                select(User)
                .where(User.tg_id == event.from_user.id)
            )).scalar()

            if user is not None and user.last_seen != datetime.today().date():
                user.last_seen = datetime.today().date()
                user = await session.merge(user)
                await session.commit()

            data['user'] = user

            admin: Admin = (await session.execute(
                select(Admin)
                .where(Admin.tg_id == event.from_user.id)
            )).scalar()
            data['admin'] = admin

            return await handler(event, data)