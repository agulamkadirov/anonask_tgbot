from aiogram import Router, F, Bot
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup,
)

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, UserStep
from bot.filters import user_step
from bot.messages import MESSAGE_TEXT


router = Router()


@router.message(
    F.text, user_step(UserStep.SEND_ANSWER)
)
async def send_answer(
    message: Message,
    bot: Bot,
    user: User,
    ref_link: str,
    session: AsyncSession,
) -> None:
    ref_link += str(user.tg_id)
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Yana yozish", url=ref_link)
            ]
        ]
    )
    await bot.send_message(
        user.chat_with, MESSAGE_TEXT['answer'].format(message.text),
        entities=message.entities,
        reply_markup=btn,
    )

    user.step = UserStep.FREE
    await session.merge(user)
    await session.commit()

    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['answer_sent'],
    )


# matn bo'lmagan xabarlar uchun:
# duplikaaaaaaat
# TODO: duplikat fix
@router.message(
    user_step(UserStep.SEND_ANSWER)
)
async def send_answer2(
    message: Message,
    bot: Bot,
    user: User,
    ref_link: str,
    session: AsyncSession,
) -> None:
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Yana yozish", url=ref_link)
            ]
        ]
    )

    await bot.send_message(
        user.chat_with, MESSAGE_TEXT['answer2'],
    )
    await bot.copy_message(
        user.chat_with, user.tg_id,
        message.message_id,
        reply_markup=btn,
    )

    user.step = UserStep.FREE
    await session.merge(user)
    await session.commit()

    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['answer_sent'],
    )