from aiogram import Router, F
from aiogram.types import Message

from app.bot.manager import Manager

router = Router()
router.message.filter(F.chat.type == "private")


@router.message()
async def default_message(message: Message, manager: Manager) -> None:
    await manager.delete_message(message)
