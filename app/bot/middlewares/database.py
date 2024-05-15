from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import UserDB


class DBSessionMiddleware(BaseMiddleware):
    """
    Middleware for handling database sessions.
    """

    def __init__(self, sessionmaker: async_sessionmaker):
        """
        Initialize the DBSessionMiddleware.

        :param sessionmaker: The SQLAlchemy sessionmaker object.
        """
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Call the middleware.

        :param handler: The handler function.
        :param event: The Telegram event.
        :param data: Additional data.
        """
        user: User = data.get("event_from_user")
        if user is not None:
            user_db = await UserDB.create_or_update(
                self.sessionmaker,
                id=user.id,
                full_name=user.full_name,
                username=f"@{user.username}",
            )
            # Pass the user_db to the handler function
            data["user_db"] = user_db

        # Pass the async_sessionmaker to the handler function
        data["sessionmaker"] = self.sessionmaker

        # Call the handler function with the event and data
        return await handler(event, data)
