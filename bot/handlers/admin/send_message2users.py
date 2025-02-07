from aiogram import F, Bot, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, func

import datetime

from bot.db.models import MessageQueue, Admin, AdminSteps, User
from bot.filters import admin_step
from bot.utils import send_message_to_users

from .constants import BTN_SEND_MESSAGE_CMND, BTN_CANCEL, ADMIN_MENU


router = Router()


@router.message(
    F.text == BTN_SEND_MESSAGE_CMND,
    admin_step(AdminSteps.FREE)
)
async def ask_for_message(
    message: Message,
    bot: Bot,
    session: AsyncSession,
) -> None:
    tg_id = message.from_user.id
    await session.execute(
        update(Admin)
        .values(step=AdminSteps.SEND_MESSAGE)
        .where(Admin.tg_id == tg_id)
    )
    await session.commit()

    await bot.send_message(
        tg_id, "Jo'natilajak xabarni yozing yoki forward qiling",
        reply_markup=BTN_CANCEL,
    )

@router.message(
    admin_step(AdminSteps.SEND_MESSAGE),
    F.text != BTN_CANCEL
)
async def register_message(
    message: Message,
    bot: Bot,
    session: AsyncSession
) -> None:
    tg_id = message.from_user.id
    await session.merge(
        MessageQueue(
            chat_id=tg_id, message_id=message.message_id,
        )
    )
    await session.execute(
        update(Admin)
        .values(step=AdminSteps.FREE)
        .where(Admin.tg_id == tg_id)
    )
    await session.commit()
    users_count = (await session.execute(
        func.count(User.tg_id)
    )).scalar()

    est_time = datetime.timedelta(seconds=users_count / 30)
    est_time_str = str(
        est_time - datetime.timedelta(microseconds=est_time.microseconds)
    )
    await bot.send_message(
        tg_id,
        f"Xabar foydalanuvchilarga yuborilmoqda.\nTaxminiy kutish vaqti: {est_time_str}",
        reply_markup=ADMIN_MENU
    )

    await send_message_to_users(bot, session)