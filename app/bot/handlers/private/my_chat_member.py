from aiogram import Router, F
from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import UserDB

router = Router()
router.my_chat_member.filter(F.chat.type == "private")


@router.my_chat_member()
async def my_chat_member(update: ChatMemberUpdated,
                         sessionmaker: async_sessionmaker,
                         user_db: UserDB) -> None:
    """
    Handle updates of the bot chat member status.

    :param update: The chat member update event.
    :param sessionmaker: The async async_sessionmaker object for creating database sessions.
    :param user_db: The user object from database.
    """
    await UserDB.update(
        sessionmaker,
        primary_key=user_db.id,
        state=update.new_chat_member.status,
    )
