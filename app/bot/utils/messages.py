import asyncio
from typing import Union

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter
from aiogram.types import BufferedInputFile, Message
from aiogram.types import InlineKeyboardMarkup as Markup


async def send_message(
        bot: Bot,
        chat_id: int,
        text: Union[str, None] = None,
        document: Union[BufferedInputFile, None] = None,
        reply_markup: Union[Markup, None] = None,
) -> Union[Message, None]:
    try:
        await asyncio.sleep(0.05)
        if document:
            message = await bot.send_document(
                chat_id=chat_id,
                document=document,
                caption=text,
                reply_markup=reply_markup,
            )
        else:
            message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
            )
        return message

    except TelegramRetryAfter as e:
        # If rate limited, wait and try again
        await asyncio.sleep(e.retry_after)
        await send_message(bot, chat_id, text, document, reply_markup)
    except (TelegramBadRequest, Exception):
        # If chat is not found, or bot is blocked, or any other error, skip.
        pass
