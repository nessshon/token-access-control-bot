import asyncio

from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import or_f
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter,
    IS_ADMIN, IS_NOT_MEMBER,
)
from aiogram.types import ChatMemberUpdated, ChatJoinRequest

from app.bot.handlers.admin.windows import AdminWindow
from app.bot.handlers.chats.windows import ChatWindow
from app.bot.handlers.private.windows import Window
from app.bot.manager import Manager, SendMode
from app.bot.utils import user_is_holder
from app.db.models import AdminDB, TokenDB, MemberDB, UserDB

router = Router()
router.my_chat_member.filter(
    or_f(
        *[
            F.chat.type == ChatType.CHANNEL,
            F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
        ]
    )
)


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_ADMIN,
    ),
)
async def bot_added_to_channel(
        event: ChatMemberUpdated,
        manager: Manager,
) -> None:
    """
    Bot was added to channel.
    """
    await asyncio.sleep(1.0)

    manager = await Manager.from_user(manager.user_db.id)
    admins_ids = await AdminDB.get_all_ids(manager.sessionmaker, manager.config)

    if event.from_user.id in admins_ids:
        chat = {
            "id": event.chat.id,
            "name": event.chat.title,
            "type": event.chat.type,
        }
        await manager.state.update_data(chat=chat)
        await AdminWindow.chat_confirm_add(manager, send_mode=SendMode.SEND)


@router.chat_join_request()
async def chat_join_request(event: ChatJoinRequest, manager: Manager) -> None:
    manager = await Manager.from_user(manager.user_db.id)

    if not manager.user_db.wallet_address:
        await Window.select_language(manager, send_mode=SendMode.SEND)

    else:
        tokens = await TokenDB.all(manager.sessionmaker)
        if await user_is_holder(manager.user_db, tokens):
            await MemberDB.create_or_update(
                manager.sessionmaker,
                user_id=manager.user_db.id,
                chat_id=event.chat.id,
            )
            await event.approve()
            if event.chat.type != ChatType.CHANNEL:
                user = await UserDB.get(manager.sessionmaker, event.from_user.id)
                text = manager.text_message.get("welcome_to_chat")
                await ChatWindow.balance(event, manager, user, text)

        else:
            await Window.deny_access(manager, send_mode=SendMode.SEND)
            await event.decline()


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER,
    ),
    F.new_chat_member.user.is_bot.is_(False),
)
async def bot_left_from_channel(event: ChatMemberUpdated, manager: Manager) -> None:
    """
    Member was left from channel.
    """
    await MemberDB.delete_by_filter(
        manager.sessionmaker,
        user_id=event.from_user.id,
        chat_id=event.chat.id,
    )
