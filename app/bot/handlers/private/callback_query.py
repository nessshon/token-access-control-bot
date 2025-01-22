from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram_newsletter.manager import ANManager
from aiogram_tonconnect import ATCManager
from aiogram_tonconnect.tonconnect.models import ConnectWalletCallbacks

from app.bot.handlers.private.windows import Window
from app.bot.manager import Manager
from app.bot.utils import user_is_holder
from app.bot.utils.states import UserState
from app.bot.utils.texts import TextMessage, TextButton
from app.db.models import UserDB, TokenDB
from app.texts import SUPPORTED_LANGUAGES

router = Router()
router.callback_query.filter(F.message.chat.type == "private")


@router.callback_query(StateFilter("*"), F.data == "main")
async def main_callback_query(call: CallbackQuery, manager: Manager) -> None:
    if not manager.user_db.wallet_address:
        await Window.select_language(manager)
    else:
        await Window.main_menu(manager)
    await call.answer()


@router.callback_query(UserState.SELECT_LANGUAGE)
async def select_language_callback_query(
        call: CallbackQuery,
        manager: Manager,
        atc_manager: ATCManager,
        an_manager: ANManager,
) -> None:
    if call.data in list(SUPPORTED_LANGUAGES.keys()):
        await manager.send_loader_message()

        await UserDB.update(
            manager.sessionmaker,
            primary_key=manager.user_db.id,
            language_code=call.data,
        )
        await atc_manager.update_interfaces_language(call.data)
        await an_manager.update_interfaces_language(call.data)
        manager.text_message = TextMessage(call.data)
        manager.text_button = TextButton(call.data)

        await atc_manager.connect_wallet(
            callbacks=ConnectWalletCallbacks(
                before_callback=Window.select_language,
                after_callback=Window.main_menu,
            ),
        )

    await call.answer()


@router.callback_query(UserState.MAIN_MENU)
async def main_menu_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data == "get_access":
        await manager.send_loader_message()

        tokens = await TokenDB.all(manager.sessionmaker)

        if await user_is_holder(manager.user_db, tokens):
            await Window.allow_access(manager)
        else:
            await Window.deny_access(manager)

    elif call.data == "disconnect_wallet":
        await manager.send_loader_message()

        await UserDB.update(
            manager.sessionmaker,
            primary_key=manager.user_db.id,
            wallet_address=None,
        )
        await atc_manager.disconnect_wallet()
        await Window.select_language(manager)

    elif call.data == "change_language":
        await Window.change_language(manager)

    await call.answer()


@router.callback_query(UserState.CHANGE_LANGUAGE)
async def change_language_callback_query(call: CallbackQuery, manager: Manager, atc_manager: ATCManager) -> None:
    if call.data in list(SUPPORTED_LANGUAGES.keys()):
        await UserDB.update(
            manager.sessionmaker,
            primary_key=manager.user_db.id,
            language_code=call.data,
        )
        await atc_manager.update_interfaces_language(call.data)
        manager.text_message = TextMessage(call.data)
        manager.text_button = TextButton(call.data)

        await Window.main_menu(manager)

    await call.answer()
