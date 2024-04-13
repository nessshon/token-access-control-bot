from __future__ import annotations

from aiogram.enums import ChatMemberStatus
from sqlalchemy import *

from ._abc import AbstractModel


class UserDB(AbstractModel):
    __tablename__ = "users"

    class State:
        MEMBER = ChatMemberStatus.MEMBER
        KICKED = ChatMemberStatus.KICKED

    id = Column(
        BigInteger,
        nullable=False,
        primary_key=True,
    )
    state = Column(
        VARCHAR(length=6),
        nullable=False,
        default=State.MEMBER,
    )
    full_name = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    language_code = Column(
        VARCHAR(length=2),
        nullable=True,
    )
    username = Column(
        VARCHAR(length=32),
        nullable=True,
    )
    wallet_address = Column(
        VARCHAR(length=48),
        nullable=True,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
