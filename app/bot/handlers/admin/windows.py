from aiogram.types import User
from aiogram.utils.markdown import hcode, hbold
from pytonapi.exceptions import TONAPIError
from pytonapi.schema.accounts import Account
from pytonapi.schema.jettons import JettonInfo
from pytonapi.schema.nft import NftCollection

from app.bot.manager import Manager, SendMode
from app.bot.utils import keyboards
from app.bot.utils.states import AdminState
from app.bot.utils.urls import TonviewerUrl
from app.db.models import ChatDB, TokenDB, AdminDB


class AdminWindow:

    @staticmethod
    async def admin_menu(manager: Manager, send_mode: SendMode = SendMode.EDIT, **_) -> None:
        text = manager.text_message.get("admin_menu")
        reply_markup = keyboards.admin_menu(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.ADMIN_MENU)

    @staticmethod
    async def chats_menu(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        page, page_size = state_data.get("page", 1), 5
        db_items = await ChatDB.paginate(
            manager.sessionmaker,
            page_number=page,
            page_size=page_size,
            order_by=ChatDB.id.desc(),
        )
        total_pages = await ChatDB.total_pages(
            manager.sessionmaker,
            page_size=page_size,
        )
        pagination = keyboards.InlineKeyboardPaginator(
            [(i.name, i.id) for i in db_items],
            current_page=page,
            total_pages=total_pages,
            after_reply_markup=keyboards.back(manager.text_button),
        )
        text = manager.text_message.get("chats_menu")
        reply_markup = pagination.as_markup()

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.CHATS_MENU)

    @staticmethod
    async def chat_info(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        chat = await ChatDB.get(manager.sessionmaker, state_data.get("chat_id"))

        text = manager.text_message.get("chat_info").format(
            chat_id=hcode(chat.id),
            chat_type=chat.type,
            chat_name=hbold(chat.name),
            chat_invite_link=chat.invite_link,
            chat_created_at=hcode(chat.created_at.strftime("%Y-%m-%d %H:%M")),
        )
        reply_markup = keyboards.back_delete(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.CHAT_INFO)

    @staticmethod
    async def chat_confirm_delete(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()

        chat = await ChatDB.get(manager.sessionmaker, state_data.get("chat_id"))
        text = manager.text_message.get("confirm_item_delete").format(
            item=chat.name, table=ChatDB.__tablename__.title(),
        )
        reply_markup = keyboards.back_confirm(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.CHAT_CONFIRM_DELETE)

    @staticmethod
    async def chat_confirm_add(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        chat = state_data.get("chat")

        text = manager.text_message.get("confirm_item_add").format(
            item=chat["name"], table=ChatDB.__tablename__.title(),
        )
        reply_markup = keyboards.back_confirm(manager.text_button)

        msg = await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.update_data(message_id=msg.message_id)
        await manager.state.set_state(AdminState.CHAT_CONFIRM_ADD)

    @staticmethod
    async def tokens_menu(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        page, page_size = state_data.get("page", 1), 5
        db_items = await TokenDB.paginate(
            manager.sessionmaker,
            page_number=page,
            page_size=page_size,
            order_by=TokenDB.id.desc(),
        )
        total_pages = await TokenDB.total_pages(
            manager.sessionmaker,
            page_size=page_size,
        )
        pagination = keyboards.InlineKeyboardPaginator(
            [(i.name, i.id) for i in db_items],
            current_page=page,
            total_pages=total_pages,
            after_reply_markup=keyboards.back_add(manager.text_button),
        )
        text = manager.text_message.get("tokens_menu")
        reply_markup = pagination.as_markup()

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKENS_MENU)

    @staticmethod
    async def token_info(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        token = await TokenDB.get(manager.sessionmaker, state_data.get("token_id"))

        tonviewer_url = TonviewerUrl(token.address, token.name)
        text = manager.text_message.get("token_info").format(
            token_name=token.name,
            token_type=token.type,
            token_min_amount=token.min_amount,
            token_address=tonviewer_url.hlink_short,
            token_created_at=token.created_at.strftime("%Y-%m-%d %H:%M"),
        )
        reply_markup = keyboards.token_info(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKEN_INFO)

    @staticmethod
    async def token_confirm_delete(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()

        token = await TokenDB.get(manager.sessionmaker, state_data.get("token_id"))
        text = manager.text_message.get("confirm_item_delete").format(
            item=token.name, table=TokenDB.__tablename__.title(),
        )
        reply_markup = keyboards.back_confirm(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKEN_CONFIRM_DELETE)

    @staticmethod
    async def token_send_address(
            manager: Manager,
            additional_text: str = None,
            send_mode: SendMode = SendMode.EDIT,
    ) -> None:
        text = manager.text_message.get("token_send_address")
        if additional_text:
            text += f"\n\n{additional_text}"
        reply_markup = keyboards.back(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKEN_SEND_ADDRESS)

    @staticmethod
    async def token_send_amount(
            manager: Manager,
            additional_text: str = None,
            send_mode: SendMode = SendMode.EDIT,
    ) -> None:
        state_data = await manager.state.get_data()
        account = Account(**state_data.get("account"))

        token_type = state_data.get("token_type")
        if token_type == TokenDB.Type.JettonMaster:
            token = JettonInfo(**state_data.get("token"))
            if not token.metadata:
                raise TONAPIError("TONAPI Error: Token metadata not indexed.")
            token_name = f"{token.metadata.name} [{token.metadata.symbol}]"
        else:
            token = NftCollection(**state_data.get("token"))
            if not token.metadata:
                raise TONAPIError("TONAPI Error: Token metadata not indexed.")
            token_name = token.metadata.get("name", "Unknown Collection")

        tonviewer_url = TonviewerUrl(account.address.to_userfriendly(True), token_name)
        text = manager.text_message.get("token_send_amount").format(
            token_name=tonviewer_url.hlink_name,
            token_type=token_type,
        )
        if additional_text:
            text += f"\n\n{additional_text}"
        reply_markup = keyboards.back(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKEN_SEND_AMOUNT)

    @staticmethod
    async def token_confirm_add(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        account = Account(**state_data.get("account"))

        token_type = state_data.get("token_type")
        if token_type == TokenDB.Type.JettonMaster:
            token = JettonInfo(**state_data.get("token"))
            token_name = f"{token.metadata.name} [{token.metadata.symbol}]"
        else:
            token = NftCollection(**state_data.get("token"))
            token_name = token.metadata.get("name", "Unknown Collection")
        tonviewer_url = TonviewerUrl(account.address.to_userfriendly(True), token_name)

        text = manager.text_message.get("confirm_item_add").format(
            item=tonviewer_url.hlink_name, table=TokenDB.__tablename__.title(),
        )
        reply_markup = keyboards.back_confirm(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKEN_CONFIRM_ADD)

    @staticmethod
    async def token_edit_amount(
            manager: Manager,
            additional_text: str = None,
            send_mode: SendMode = SendMode.EDIT
    ) -> None:
        text = manager.text_message.get("token_edit_amount")
        if additional_text:
            text += f"\n\n{additional_text}"
        reply_markup = keyboards.back(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.TOKEN_EDIT_AMOUNT)

    @staticmethod
    async def admins_menu(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        page, page_size = state_data.get("page", 1), 5
        items = await AdminDB.paginate(
            manager.sessionmaker,
            page_number=page,
            page_size=page_size,
            order_by=AdminDB.id.desc(),
            join_tables=[AdminDB.user],
        )
        total_pages = await AdminDB.total_pages(
            manager.sessionmaker,
            page_size=page_size,
        )
        pagination = keyboards.InlineKeyboardPaginator(
            [(i.user.full_name, i.id) for i in items],
            current_page=page,
            total_pages=total_pages,
            after_reply_markup=keyboards.back_add(manager.text_button),
        )
        reply_markup = pagination.as_markup()
        text = manager.text_message.get("admins_menu")

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.ADMINS_MENU)

    @staticmethod
    async def admin_info(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        admin = await AdminDB.get_with_join(
            manager.sessionmaker,
            primary_key=state_data.get("admin_id"),
            join_tables=[AdminDB.user],
        )

        text = manager.text_message.get("admin_info").format(
            admin_id=hcode(admin.user.id),
            admin_username=admin.user.username,
            admin_full_name=hbold(admin.user.full_name),
            admin_created_at=hcode(admin.created_at.strftime("%Y-%m-%d %H:%M")),
        )
        reply_markup = keyboards.back_delete(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.ADMIN_INFO)

    @staticmethod
    async def admin_confirm_delete(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        admin = await AdminDB.get_with_join(
            manager.sessionmaker,
            primary_key=state_data.get("admin_id"),
            join_tables=[AdminDB.user],
        )

        text = manager.text_message.get("confirm_item_delete").format(
            item=admin.user.full_name, table=AdminDB.__tablename__.title(),
        )
        reply_markup = keyboards.back_confirm(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.ADMIN_CONFIRM_DELETE)

    @staticmethod
    async def admin_send_id(
            manager: Manager,
            additional_text: str = None,
            send_mode: SendMode = SendMode.EDIT,
    ) -> None:
        text = manager.text_message.get("admin_send_id")
        if additional_text:
            text += f"\n\n{additional_text}"
        reply_markup = keyboards.back(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.ADMIN_SEND_ID)

    @staticmethod
    async def admin_confirm_add(manager: Manager, send_mode: SendMode = SendMode.EDIT) -> None:
        state_data = await manager.state.get_data()
        user = User(**state_data.get("user"))

        text = manager.text_message.get("confirm_item_add").format(
            item=user.full_name, table=AdminDB.__tablename__.title(),
        )
        reply_markup = keyboards.back_confirm(manager.text_button)

        await manager.send_message(text, reply_markup=reply_markup, send_mode=send_mode)
        await manager.state.set_state(AdminState.ADMIN_CONFIRM_ADD)
