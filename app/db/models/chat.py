from __future__ import annotations

from sqlalchemy import *

from ._abc import AbstractModel


class ChatDB(AbstractModel):
    __tablename__ = "chats"

    id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    type = Column(
        VARCHAR(length=32),
        nullable=False,
    )
    invite_link = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
