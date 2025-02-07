from aiogram import F, Router, Bot
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
)

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, UserStep
from bot.messages import MESSAGE_TEXT


router = Router()

@router.callback_query(
    F.data.regexp('cancel')
)
async def cancel_message(
    cq: CallbackQuery,
    bot: Bot,
    user: User,
    session: AsyncSession
) -> None:
    await cq.message.delete()
    
    user.step = UserStep.FREE
    await session.merge(user)
    await session.commit()

    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['message_cancelled'],
    )


@router.callback_query(
    F.data.regexp(r"answer \d+")
)
async def answer_to(
    cq: CallbackQuery,
    bot: Bot,
    user: User,
    session: AsyncSession
) -> None:
    chat_with = int(cq.data.split()[-1])
    user.chat_with = chat_with
    user.step = UserStep.SEND_ANSWER
    await session.merge(user)
    await session.commit()

    # bilaman shu knopka start dagi duplikat
    # TODO: duplikat
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data='cancel')
            ]
        ]
    )

    await cq.answer('Javobingizni yozing')
    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['send_answer'],
        reply_markup=btn
    )