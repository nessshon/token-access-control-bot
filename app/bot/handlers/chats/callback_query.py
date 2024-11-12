from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.types import CallbackQuery

from app.bot.handlers.chats.windows import ChatWindow
from app.bot.manager import Manager, SendMode

router = Router()
router.callback_query.filter(
    F.message.chat.type.in_(
        [
            ChatType.GROUP,
            ChatType.SUPERGROUP,
        ]
    )
)


@router.callback_query()
async def top_list_callback_query(call: CallbackQuery, manager: Manager) -> None:
    token_id, page = call.data.split(":")

    await ChatWindow.top_list(
        message=call.message,
        manager=manager,
        token_id=int(token_id),
        page=int(page),
        send_mode=SendMode.EDIT,
    )
