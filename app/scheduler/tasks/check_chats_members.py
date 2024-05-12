import asyncio
import logging
from typing import Sequence

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.handlers.private.windows import Window
from app.bot.manager import Manager, SendMode
from app.bot.utils import user_is_holder, kick_member
from app.db.models import ChatDB, TokenDB, MemberDB


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
        if await user_is_holder(member.user, tokens):
            continue

        try:
            await kick_member(bot, member)
            await MemberDB.delete(sessionmaker, primary_key=member.id)

            manager = await Manager.from_user(member.user_id)
            await Window.deny_access(manager, send_mode=SendMode.SEND)
        except Exception as e:
            logging.error(e)
