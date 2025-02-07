from aiogram import Router, Bot, F
from aiogram.types import (
    Message,
)

from bot.db.models import Admin, AdminSteps
from bot.messages import MESSAGE_TEXT
from bot.handlers.user.start import say_hi

from sqlalchemy.ext.asyncio import AsyncSession

from .constants import BTN_CANCEL_CMND, ADMIN_MENU


router = Router()


@router.message(
    (F.text == '/start') | (F.text == BTN_CANCEL_CMND)
)
async def admin_started(
    message: Message,
    bot: Bot,
    session: AsyncSession,
    ref_link: str,
) -> None:
    admin = Admin(
        tg_id = message.from_user.id,
        step=AdminSteps.FREE
    )
    admin = (await session.merge(admin))
    await session.commit()

    await say_hi(message, bot, ref_link, session)
    await bot.send_message(
        message.from_user.id, "Asosiy menyu",
        reply_markup=ADMIN_MENU
    )