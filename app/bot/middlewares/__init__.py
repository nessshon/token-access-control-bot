from aiogram import Dispatcher
from aiogram_newsletter.middleware import AiogramNewsletterMiddleware
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware
from aiogram_tonconnect.tonconnect.storage.base import ATCRedisStorage
from aiogram_tonconnect.utils.qrcode import QRUrlProvider
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from .database import DBSessionMiddleware
from .manager import ManagerMiddleware
from .throttling import ThrottlingMiddleware
from ..utils.keyboards import AiogramTonconnectInlineKeyboard
from ..utils.texts import AiogramTonconnectTextMessage
from ...config import Config
from ...scheduler import Scheduler


def bot_middlewares_register(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    redis: Redis = kwargs["redis"]
    config: Config = kwargs["config"]
    scheduler: Scheduler = kwargs["scheduler"]
    sessionmaker: async_sessionmaker = kwargs["sessionmaker"]

    dp.update.outer_middleware.register(
        AiogramTonConnectMiddleware(
            storage=ATCRedisStorage(redis),
            manifest_url=config.MANIFEST_URL,
            text_message=AiogramTonconnectTextMessage,
            inline_keyboard=AiogramTonconnectInlineKeyboard,
            qrcode_provider=QRUrlProvider(),
            tonapi_token=config.tonapi.TONCONNECT_KEY,
        )
    )

    dp.update.outer_middleware.register(DBSessionMiddleware(sessionmaker))
    dp.update.outer_middleware.register(ThrottlingMiddleware())
    dp.update.outer_middleware.register(ManagerMiddleware())

    dp.update.middleware.register(AiogramNewsletterMiddleware(scheduler.new(2)))


__all__ = [
    "bot_middlewares_register",
]
