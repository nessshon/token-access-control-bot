from contextlib import suppress
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand, BotCommandScopeChat


async def bot_commands_setup(bot: Bot, admins_ids: List[int]) -> None:
    """
    Setup bot commands.

    :param bot: The Bot object.
    :param admins_ids: List of admin IDs.
    """
    commands = {
        "en": [
            BotCommand(command="start", description="Restart bot"),
        ],
        "ru": [
            BotCommand(command="start", description="Перезапустить бота"),
        ]
    }
    admin_commands = {
        "en": [
            BotCommand(command="admin", description="Admin panel"),
        ],
        "ru": [
            BotCommand(command="admin", description="Панель администратора"),
        ]
    }

    # Set commands for all private chats in English language
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )
    # Set commands for all private chats in Russian language
    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru"
    )

    # Set commands for all admin chats
    for admin_id in admins_ids:
        with suppress(TelegramBadRequest):
            await bot.set_my_commands(
                commands=commands["en"] + admin_commands["en"],
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        with suppress(TelegramBadRequest):
            await bot.set_my_commands(
                commands=commands["ru"] + admin_commands["ru"],
                scope=BotCommandScopeChat(chat_id=admin_id),
                language_code="ru"
            )


async def bot_commands_delete(bot: Bot, admins_ids: List[int]) -> None:
    """
    Delete bot commands.

    :param bot: The Bot object.
    :param admins_ids: List of admin IDs.
    """

    # Delete commands for all private chats in any language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
    )
    # Delete commands for all private chats in Russian language
    await bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru",
    )

    # Delete commands for all admin chats
    for admin_id in admins_ids:
        with suppress(TelegramBadRequest):
            await bot.delete_my_commands(
                scope=BotCommandScopeChat(chat_id=admin_id)
            )
        with suppress(TelegramBadRequest):
            await bot.delete_my_commands(
                scope=BotCommandScopeChat(chat_id=admin_id),
                language_code="ru"
            )
