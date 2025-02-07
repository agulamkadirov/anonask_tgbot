from aiogram import Router, F

from . import (
    anon_message,
    start,
    callback_handler,
    answer
)


router = Router()
router.message.filter(F.chat.type == 'private')

router.include_routers(
        start.router,
        anon_message.router,
        callback_handler.router,
        answer.router
)


__all__ = [
    'router'
]