from aiogram import Router, F, Bot
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from bot.filters import admin_step
from bot.db.models import AdminSteps, User

from .constants import BTN_GET_STATS_CMND
from datetime import datetime, timedelta

router = Router()


@router.message(
    F.text == BTN_GET_STATS_CMND,
    admin_step(AdminSteps.FREE)
)
async def get_stats(
    message: Message,
    bot: Bot,
    session: AsyncSession
) -> None:
    total_users: int = (
        await session.execute(
            func.count(User.tg_id)
        )
    ).scalar()
    
    txt = f"Foydalanuvchilar: {total_users}\n"

    dt = datetime.today().date()
    for i in range(7):
        active_users = (await session.execute(
            select(func.count(User.tg_id))
            .where(User.last_seen == dt)
        )).scalar()

        txt += f"\n— {active_users} ta(<b>{dt.strftime('%d-%m-%Y')}</b>)"
        dt = dt - timedelta(days=1)

    await bot.send_message(
        message.from_user.id,
        txt,
    )