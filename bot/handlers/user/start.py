from aiogram import F, Bot, Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, UserStep

from bot.messages import MESSAGE_TEXT


router = Router()


@router.message(
    F.text == '/start'
)
async def say_hi(
    message: Message,
    bot: Bot,
    ref_link: str,
    session: AsyncSession,
) -> None:
    user = User(
        tg_id=message.from_user.id,
        step=UserStep.FREE,
        last_seen=message.date.date()
    )
    await session.merge(user)
    await session.commit()

    ref_link += str(user.tg_id)
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔗 Havolani ulashish",
                    url=f"https://t.me/share/url?url={ref_link}"
                )
            ]
        ]
    )
    await bot.send_message(
        message.from_user.id, MESSAGE_TEXT['say_hi'].format(ref_link),
        reply_markup=btn
    )


# Invitation link bilan start bosganda
@router.message(
    F.text.regexp(r'/start \d+')
)
async def start_anon_chat(
    message: Message,
    bot: Bot,
    user: User | None, # None bo'lishi ham mumkin
    session: AsyncSession
) -> None:
    if user is None:
        user = User(tg_id=message.from_user.id, last_seen=message.date.date())

    chat_with_id = int(message.text.split()[-1])
    if chat_with_id == user.tg_id:
        await bot.send_message(
            user.tg_id, MESSAGE_TEXT['no_self_messaging']
        )
        return
    
    user.chat_with = chat_with_id
    user.step = UserStep.SEND_ANON_MSG

    await session.merge(user)
    await session.commit()

    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data='cancel')
            ]
        ]
    )

    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['send_anon_msg'],
        reply_markup=btn
    )
