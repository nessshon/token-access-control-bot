from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.markdown import hcode
from pytonapi import AsyncTonapi

from app.db.models import TokenDB
from ._filters import AdminFilter
from .windows import AdminWindow
from ...manager import Manager
from ...utils.states import AdminState
from ...utils.validations import is_float

router = Router()
router.message.filter(F.chat.type == "private", AdminFilter())


@router.message(AdminState.TOKEN_SEND_ADDRESS)
async def token_send_address_message(message: Message, manager: Manager, tonapi: AsyncTonapi) -> None:
    if message.content_type == "text":
        await manager.send_loader_message()

        try:
            account = await tonapi.accounts.get_info(message.text)

            if await TokenDB.exists_by_filter(manager.sessionmaker, address=account.address.to_userfriendly(True)):
                raise ValueError(
                    manager.text_message.get("token_send_address_error_already_exist").format(
                        address=account.address.to_userfriendly(True),
                    )
                )

            if "jetton_master" in account.interfaces or "nft_collection" in account.interfaces:
                if "jetton_master" in account.interfaces:
                    token_type = TokenDB.Type.JettonMaster
                    token = await tonapi.jettons.get_info(account.address.to_raw())
                else:
                    token_type = TokenDB.Type.NFTCollection
                    token = await tonapi.nft.get_collection_by_collection_address(account.address.to_raw())

                await manager.state.update_data(account=account.model_dump(), token=token.model_dump(), token_type=token_type)
                await AdminWindow.token_send_amount(manager)
            else:
                raise ValueError(
                    manager.text_message.get("token_send_address_error_not_supported").format(
                        supported_interfaces=", ".join(TokenDB.Type.values()),
                        interfaces=", ".join(account.interfaces),
                    )
                )

        except Exception as e:
            text = manager.text_message.get("token_send_address_error")
            await AdminWindow.token_send_address(manager, text.format(hcode(e)))

    await manager.delete_message(message)


@router.message(AdminState.TOKEN_SEND_AMOUNT)
async def token_send_amount_message(message: Message, manager: Manager) -> None:
    if message.content_type == "text":
        state_data = await manager.state.get_data()
        token_type = state_data.get("token_type")

        min_amount = (
            float(message.text.replace(",", "."))
            if is_float(message.text)
            else None
        )

        if min_amount and token_type == TokenDB.Type.NFTCollection and not min_amount.is_integer():
            min_amount = int(min_amount)

        if min_amount and min_amount > 0:
            await manager.state.update_data(token_min_amount=min_amount)
            await AdminWindow.token_confirm_add(manager)

        else:
            text = manager.text_message.get("token_send_amount_error")
            await AdminWindow.token_send_amount(manager, text)

    await manager.delete_message(message)


@router.message(AdminState.TOKEN_EDIT_AMOUNT)
async def token_edit_amount_message(message: Message, manager: Manager) -> None:
    if message.content_type == "text":
        state_data = await manager.state.get_data()
        token = await TokenDB.get(manager.sessionmaker, state_data.get("token_id"))

        min_amount = (
            float(message.text.replace(",", "."))
            if is_float(message.text)
            else None
        )

        if min_amount and token.type == TokenDB.Type.NFTCollection and not min_amount.is_integer():
            min_amount = int(min_amount)

        if min_amount and min_amount > 0:
            await TokenDB.update(
                manager.sessionmaker,
                primary_key=token.id,
                min_amount=min_amount,
            )
            await AdminWindow.token_info(manager)

        else:
            text = manager.text_message.get("token_send_amount_error")
            await AdminWindow.token_edit_amount(manager, text)

    await manager.delete_message(message)


@router.message(AdminState.ADMIN_SEND_ID)
async def admin_send_id_message(message: Message, manager: Manager) -> None:
    if message.content_type == "text":
        try:
            if message.text.isdigit():
                try:
                    chat = await manager.bot.get_chat_member(
                        chat_id=int(message.text), user_id=int(message.text),
                    )
                except Exception:
                    raise ValueError(manager.text_message.get("admin_send_id_error_not_found"))

                await manager.state.update_data(admin_id=int(message.text), user=chat.user.model_dump())
                await AdminWindow.admin_confirm_add(manager)

            else:
                raise ValueError(manager.text_message.get("admin_send_id_error_not_member"))

        except Exception as e:
            text = manager.text_message.get("admin_send_id_error")
            await AdminWindow.admin_send_id(manager, text.format(hcode(e)))

    await manager.delete_message(message)
