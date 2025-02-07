from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
from aiogram import Bot

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult, update, func, delete

from typing import List

from bot.db.models import MessageQueue, User

from asyncio import sleep as asleep
import datetime


async def send_message_to_users(
    bot: Bot,
    session: AsyncSession
) -> None:
    last_message = (await session.execute(
        select(MessageQueue).
        where(MessageQueue.completed==False).
        order_by(MessageQueue.id.desc()).limit(1)
    )).scalar()
    if last_message is None:
        return
    
    USER_LIMIT = 100
    while True:
        users: ScalarResult = (await session.execute(
            select(User)
            .limit(USER_LIMIT)
            .offset(last_message.user_offset)
        )).scalars()
        sent = False

        for user in users:
            sent = True
            try:
                await bot.copy_message(
                    user.tg_id,
                    last_message.chat_id,
                    last_message.message_id,
                )
                last_message.received_users += 1
                await asleep(0.04)
            except Exception as e:
                # xabar yetib bormagan holatda
                # bloklagan bo'ladi
                pass

        last_message.user_offset += 100
        await session.execute(
            update(MessageQueue).
            where(MessageQueue.id == last_message.id).
            values(received_users=last_message.received_users,
                   user_offset=last_message.user_offset)
        )
        await session.commit()
    
        if not sent:
            break

    await session.execute(
        update(MessageQueue).
        where(MessageQueue.id == last_message.id).
        values(completed=True))
    await session.commit()
    users_count = (await session.execute(func.count(User.tg_id))).scalar()
    txt = """foydalanuvchilarga xabar yetkazildi:
{} ta foydalanuvchidan {} tasi xabarni oldi.
    """.format(users_count, last_message.received_users)
    await bot.send_message(
        last_message.chat_id,
        txt,
        reply_to_message_id=last_message.message_id
    )
    await send_message_to_users(bot, session)