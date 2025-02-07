from aiogram import F
from aiogram.filters import Filter
from aiogram.types import Message

from bot.db.models import User, UserStep, AdminSteps, Admin

from config import ADMIN


class FUserStep(Filter):
    def __init__(self, step: UserStep) -> None:
        self.step = step
    
    async def __call__(
            self,
            _: Message,
            user: User
    ) -> bool:
        return user is not None and user.step == self.step

# duplikat :(
# TODO fix duplikat Admin_step
class FAdminStep(Filter):
    def __init__(self, step: AdminSteps):
        self.step = step
    
    async def __call__(
            self,
            message: Message,
            admin: Admin
    ) -> bool:
        return admin is not None and admin.step == self.step



user_step = lambda step: FUserStep(step)
is_admin = F.chat.func(lambda chat: chat.id == ADMIN)
admin_step = lambda step: FAdminStep(step)

__all__ = [
    "user_step",
    "is_admin",
    "admin_step"
]