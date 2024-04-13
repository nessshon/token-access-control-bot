from typing import Union, Any, Dict

from aiogram.filters import BaseFilter
from aiogram.types import Message, User
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config import Config
from app.db.models import AdminDB


class AdminFilter(BaseFilter):

    async def __call__(
            self,
            message: Message,
            event_from_user: User,
            sessionmaker: async_sessionmaker,
            config: Config,
    ) -> Union[bool, Dict[str, Any]]:
        """ Check if the user is an admin. """
        admins_ids = await AdminDB.get_all_ids(sessionmaker, config)

        return event_from_user.id in admins_ids
