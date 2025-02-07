from aiogram import Router

from bot.filters import is_admin

from . import (
    get_stats,
    send_message2users,
    start,
)


router = Router()
router.message.filter(is_admin)

router.include_routers(
    start.router,
    get_stats.router,
    send_message2users.router,
)


__all__ = [
    'router'
]