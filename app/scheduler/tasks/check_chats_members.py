import asyncio
import logging
from contextlib import suppress
from typing import Sequence

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hlink
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.handlers.private.windows import Window
from app.bot.manager import Manager, SendMode
from app.bot.utils import user_is_holder, kick_member
from app.bot.utils.texts import TextMessage
from app.bot.utils.urls import TonviewerUrl
from app.db.models import ChatDB, TokenDB, MemberDB, UserDB


async def check_chats_members() -> None:
    loop = asyncio.get_event_loop()
    bot: Bot = loop.__getattribute__("bot")
    sessionmaker: async_sessionmaker = loop.__getattribute__("sessionmaker")

    chats = await ChatDB.all(sessionmaker)
    tokens = await TokenDB.all(sessionmaker)

    for chat in chats:
        await process_and_kick_members(sessionmaker, bot, chat, tokens)


async def process_and_kick_members(
        sessionmaker: async_sessionmaker,
        bot: Bot,
        chat: ChatDB,
        tokens: Sequence[TokenDB],
) -> None:
    members = await MemberDB.all_by_filter(
        sessionmaker,
        join_tables=[MemberDB.user],
        chat_id=chat.id,
    )

    for member in members:
        if is_any_empty_token_holders(tokens):
            logging.warning(f"Skipping check members for {chat.name} because of empty token holders!")
            break

        if await user_is_holder(member.user, tokens):
            continue

        try:
            await kick_member(bot, member)
            await send_notification_to_chat(bot, chat, member.user)
            await MemberDB.delete(sessionmaker, primary_key=member.id)

            manager = await Manager.from_user(member.user_id)
            await Window.deny_access(manager, send_mode=SendMode.SEND)
        except Exception as e:
            logging.error(e)


def is_any_empty_token_holders(tokens: Sequence[TokenDB]) -> bool:
    for token in tokens:
        if not token.holders:
            logging.warning(f"Found empty token holders on {token.name} [{token.address}]!")
            return True
    return False


async def send_notification_to_chat(bot: Bot, chat: ChatDB, user: UserDB) -> None:
    user_link = hlink(
        title=user.full_name,
        url=(
            f"https://t.me/{user.username[1:]}"
            if user.username else
            f"tg://user?id={user.id}"
        )
    )
    wallet_link = (
        TonviewerUrl(user.wallet_address).hlink_short
        if user.wallet_address else
        "N/A"
    )

    text = TextMessage(user.language_code or "en").get("user_kicked").format(
        user=user_link, wallet=wallet_link,
    )
    with suppress(TelegramBadRequest):
        await bot.send_message(chat_id=chat.id, text=text)
        await asyncio.sleep(.2)
