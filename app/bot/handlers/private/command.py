from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.handlers.private.windows import Window
from app.bot.manager import Manager, SendMode

router = Router()
router.message.filter(F.chat.type == "private")


@router.message(Command("start"))
async def start_command(message: Message, manager: Manager) -> None:
    if not manager.user_db.wallet_address:
        await Window.select_language(manager, send_mode=SendMode.SEND)

    else:
        await Window.main_menu(manager, send_mode=SendMode.SEND)

    await manager.delete_message(message)
