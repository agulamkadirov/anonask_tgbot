from sqlalchemy import (
    BigInteger, Integer, Boolean, Date, func
)
from sqlalchemy.orm import (
    Mapped, mapped_column, declarative_base
)

from enum import IntEnum
from datetime import date


Base = declarative_base()


# User state uchun old school yechim
# default aiogram'dagi states ni ishlatsak ham bo'ladi
class UserStep(IntEnum):
    FREE            =   0
    SEND_ANON_MSG   =   1
    SEND_ANSWER     =   2

class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, autoincrement=False, primary_key=True)
    chat_with: Mapped[int] = mapped_column(BigInteger, nullable=True)
    step: Mapped[int] = mapped_column(Integer)
    last_seen: Mapped[date] = mapped_column(Date, default=func.now, nullable=True)


class AdminSteps(IntEnum):
    FREE            =   0
    SEND_MESSAGE    =   1

class Admin(Base):
    __tablename__ = 'admins'

    tg_id: Mapped[int] = mapped_column(BigInteger, autoincrement=False, primary_key=True)
    step: Mapped[int] = mapped_column(Integer, default=0)

class MessageQueue(Base):
    __tablename__ = 'message_queue'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(Integer)
    user_offset: Mapped[int] = mapped_column(Integer, default=0)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    received_users: Mapped[int] = mapped_column(Integer, default=0)