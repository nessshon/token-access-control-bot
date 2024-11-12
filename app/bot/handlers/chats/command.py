from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.handlers.chats.windows import ChatWindow
from app.bot.manager import Manager, SendMode
from app.db.models import TokenDB, UserDB

router = Router()
router.message.filter(
    F.chat.type.in_(
        [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]
    )
)


@router.message(Command("balance"), F.reply_to_message & F.reply_to_message.from_user.is_bot.is_(False))
async def balance_command(message: Message, manager: Manager) -> None:
    user = await UserDB.get(manager.sessionmaker, message.reply_to_message.from_user.id)
    text = manager.text_message.get("balance_command")
    await ChatWindow.balance(message, manager, user, text)


@router.message(Command("top"))
async def top_command(message: Message, manager: Manager) -> None:
    tokens = await TokenDB.all(manager.sessionmaker)

    if len(tokens) > 1:
        await ChatWindow.top_select_token(message, manager)
    else:
        await ChatWindow.top_list(
            message=message,
            manager=manager,
            token_id=tokens[0].id,
            page=1,
            send_mode=SendMode.SEND,
        )
