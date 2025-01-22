from aiogram import Dispatcher
from aiogram_newsletter.middleware import AiogramNewsletterMiddleware
from aiogram_tonconnect.middleware import AiogramTonConnectMiddleware
from aiogram_tonconnect.utils.qrcode import QRUrlProvider
from sqlalchemy.ext.asyncio import async_sessionmaker
from tonutils.tonconnect import TonConnect

from .database import DBSessionMiddleware
from .manager import ManagerMiddleware
from .throttling import ThrottlingMiddleware
from ..utils.keyboards import AiogramTonconnectInlineKeyboard
from ..utils.texts import AiogramTonconnectTextMessage
from ...scheduler import Scheduler


def bot_middlewares_register(dp: Dispatcher, **kwargs) -> None:
    """
    Register bot middlewares.
    """
    scheduler: Scheduler = kwargs["scheduler"]
    tonconnect: TonConnect = kwargs["tonconnect"]
    sessionmaker: async_sessionmaker = kwargs["sessionmaker"]

    dp.update.outer_middleware.register(
        AiogramTonConnectMiddleware(
            tonconnect=tonconnect,
            text_message=AiogramTonconnectTextMessage,
            inline_keyboard=AiogramTonconnectInlineKeyboard,
            qrcode_provider=QRUrlProvider(),
        )
    )

    dp.update.outer_middleware.register(DBSessionMiddleware(sessionmaker))
    dp.update.outer_middleware.register(ThrottlingMiddleware())
    dp.update.outer_middleware.register(ManagerMiddleware())

    dp.update.middleware.register(AiogramNewsletterMiddleware(scheduler.new(2)))


__all__ = [
    "bot_middlewares_register",
]
