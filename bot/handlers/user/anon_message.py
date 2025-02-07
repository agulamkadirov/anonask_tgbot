from aiogram import Router, F, Bot
from aiogram.types import (
    Message, InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.utils.formatting import Text

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, UserStep
from bot.filters import user_step
from bot.messages import MESSAGE_TEXT
from config import ADMIN

from .start import say_hi


router = Router()


@router.message(
    F.text, user_step(UserStep.SEND_ANON_MSG)
)
async def send_anon_msg(
    message: Message,
    bot: Bot,
    user: User,
    ref_link: str,
    session: AsyncSession,
) -> None:
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Javob yozish", callback_data=f"answer {user.tg_id}")
            ]
        ]
    )


    txt = MESSAGE_TEXT['new_message'].format(message.text)
    if user.chat_with == ADMIN:
        txt = f"Xabar yuboruvchi: {message.from_user.first_name}(@{message.from_user.username})\n" + txt
    await bot.send_message(
        user.chat_with, txt, 
        entities=message.entities, reply_markup=btn
    )

    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['message_sent'],
    )
    # step ni say_hi ichida tozalab ketganmiz
    await say_hi(message, bot, ref_link, session)


# text bo'lmagan xabarlar uchun
# duplikat kod :(
# TODO duplikat fix
@router.message(
    user_step(UserStep.SEND_ANON_MSG)
)
async def send_anon_msg2(
    message: Message,
    bot: Bot,
    user: User,
    ref_link: str,
    session: AsyncSession,
) -> None:
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✍️ Javob yozish", callback_data=f"answer {user.tg_id}")
            ]
        ]
    )


    txt = MESSAGE_TEXT['new_message2']
    if user.chat_with == ADMIN:
        txt = f"Xabar yuboruvchi: {message.from_user.first_name}(@{message.from_user.username})\n" + txt
    # TODO agar xabar oluvchi botni bloklagan bo'lsa handle qilish kerak
    await bot.send_message(
        user.chat_with, txt, 
    )
    await bot.copy_message(
        user.chat_with, user.tg_id, message.message_id,
        reply_markup=btn,
    )

    await bot.send_message(
        user.tg_id, MESSAGE_TEXT['message_sent'],
    )
    # step ni say_hi ichida tozalab ketganmiz
    await say_hi(message, bot, ref_link, session)