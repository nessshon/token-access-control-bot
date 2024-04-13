from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ._filters import AdminFilter
from .windows import AdminWindow
from ...manager import Manager, SendMode

router = Router()
router.message.filter(F.chat.type == "private", AdminFilter())


@router.message(Command("admin"))
async def admin_command(message: Message, manager: Manager) -> None:
    await AdminWindow.admin_menu(manager, send_mode=SendMode.SEND)
    await manager.delete_message(message)
