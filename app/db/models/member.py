from __future__ import annotations

from sqlalchemy import *
from sqlalchemy.orm import relationship

from ._abc import AbstractModel


class MemberDB(AbstractModel):
    __tablename__ = "members"

    id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    user_id = Column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    chat_id = Column(
        ForeignKey(
            "chats.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
    user = relationship("UserDB", foreign_keys=[user_id], backref="user_members")
    chat = relationship("ChatDB", foreign_keys=[chat_id], backref="chat_members")
