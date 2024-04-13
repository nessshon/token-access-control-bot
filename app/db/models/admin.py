from __future__ import annotations

from typing import List

from sqlalchemy import *
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import relationship

from ._abc import AbstractModel
from ...config import Config


class AdminDB(AbstractModel):
    __tablename__ = "admins"

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
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
    user = relationship("UserDB", foreign_keys=[user_id], backref="user_admins")

    @classmethod
    async def get_all_ids(
            cls: AdminDB,
            sessionmaker: async_sessionmaker,
            config: Config,
    ) -> List[int]:
        admins = await cls.all(sessionmaker)
        admins_ids = [config.bot.DEV_ID, config.bot.ADMIN_ID]
        admins_ids += [admin.user_id for admin in admins]

        return admins_ids
