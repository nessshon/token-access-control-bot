import asyncio
import logging
from asyncio import AbstractEventLoop

from aiogram import Bot
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold, hcode
from apscheduler.events import JobExecutionEvent

from ..bot.utils.messages import send_message
from ..config import Config


async def _on_job_error(loop: AbstractEventLoop, event: JobExecutionEvent) -> None:
    """
    Handles job execution errors.

    :param event: The job execution event.
    """
    logging.exception(f"Job ID: {event.job_id}\nException: {event.exception}")

    bot: Bot = loop.__getattribute__("bot")
    config: Config = loop.__getattribute__("config")

    # Get error details
    exc_text, exc_name = str(event.exception), type(event.exception).__name__
    document_data = str(event.traceback).encode()
    document_name = f"error_{event.job_id}.txt"
    document = BufferedInputFile(document_data, filename=document_name)
    text = f"{hbold(exc_name)}:\n{hcode(exc_text[:1024 - len(exc_name) - 2])}"

    # Send document with error details
    await send_message(bot, config.bot.DEV_ID, text, document)


def on_job_error(event: JobExecutionEvent) -> None:
    """
    Handles job execution errors.

    :param event: The job execution event.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(_on_job_error(loop, event))
