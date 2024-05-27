import logging
import traceback

from aiogram import Router, F, Bot
from aiogram.types import ErrorEvent, BufferedInputFile
from aiogram.utils.markdown import hcode, hbold
from pydantic_core import PydanticSerializationError

from ..utils.messages import send_message
from ...config import Config

router = Router()


@router.errors(F.exception.message.contains("query is too old"))
async def query_too_old(_: ErrorEvent) -> None:
    """Handles errors containing 'query is too old'."""


@router.errors(F.exception.message.contains("bot was blocked by the user"))
async def bot_was_blocked_by_user(_: ErrorEvent) -> None:
    """Handles errors containing 'bot was blocked by the user'."""


@router.errors()
async def telegram_api_error(event: ErrorEvent, bot: Bot, config: Config) -> None:
    """
    Handles Telegram API errors.

    :param event: The error event.
    :param bot: The bot instance.
    :param config: The config instance.
    """
    logging.exception(f"Update: {event.update}\nException: {event.exception}")

    # Prepare data for document
    try:
        update_json = event.update.model_dump_json(indent=2, exclude_none=True)
    except PydanticSerializationError:
        return

    exc_text, exc_name = str(event.exception), type(event.exception).__name__
    update_data = str(update_json + "\n\n").encode()
    traceback_data = str(traceback.format_exc() + "\n\n").encode()

    # Send document with error details
    document_data = update_data + traceback_data
    document_name = f"error_{event.update.update_id}.txt"
    document = BufferedInputFile(document_data, filename=document_name)

    text = f"{hbold(exc_name)}:\n{hcode(exc_text[:1024 - len(exc_name) - 2])}"
    await send_message(bot, config.bot.DEV_ID, text, document)

    # Send update_json in chunks
    for text in [update_json[i:i + 4096] for i in range(0, len(update_json), 4096)]:
        await send_message(bot, config.bot.DEV_ID, hcode(text))
