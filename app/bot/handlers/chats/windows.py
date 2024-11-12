from aiogram.types import Message, TelegramObject
from aiogram.utils.markdown import hcode, hbold, hlink
from pytonapi.utils import userfriendly_to_raw

from app.bot.manager import Manager, SendMode
from app.bot.utils import amount_str, keyboards
from app.bot.utils.keyboards import InlineKeyboardPaginator
from app.bot.utils.urls import NFTBuyUrl, JettonBuyUrl
from app.db.models import TokenDB, UserDB


class ChatWindow:

    @staticmethod
    async def balance(tg_obj: TelegramObject, manager: Manager, user: UserDB, text: str) -> None:
        tokens = await TokenDB.all(manager.sessionmaker)

        if not user or not user.wallet_address:
            no_token_text = manager.text_message.get("balance_command_no_tokens")
            await tg_obj.answer(no_token_text.format(user_full_name=hbold(user.full_name)))
            return

        def format_token_name(token: TokenDB) -> str:
            url_class = NFTBuyUrl if token.type == token.Type.NFTCollection else JettonBuyUrl
            return url_class(token.address, token.name).hlink_name

        balances = [
            f"{format_token_name(token)}: {hcode(amount_str(balance))}"
            for token in tokens
            if (balance := token.holders.get(userfriendly_to_raw(user.wallet_address), 0)) > 0
        ]

        if balances:
            balance_text = "\n".join(balances)
            await tg_obj.answer(text.format(user_full_name=hbold(user.full_name), balances=balance_text))
        else:
            no_token_text = manager.text_message.get("balance_command_no_tokens")
            await tg_obj.answer(no_token_text.format(user_full_name=hbold(user.full_name)))

    @staticmethod
    async def top_select_token(message: Message, manager: Manager) -> None:
        tokens = await TokenDB.all(manager.sessionmaker)
        text = manager.text_message.get("top_select_token")
        reply_markup = keyboards.select_tokens(tokens)

        await message.answer(text, reply_markup=reply_markup)

    @staticmethod
    async def top_list(
            message: Message,
            manager: Manager,
            token_id: int,
            page: int,
            send_mode: SendMode,
    ) -> None:
        token = await TokenDB.get(manager.sessionmaker, token_id)
        users = await UserDB.all(manager.sessionmaker)

        top_holders = {
            hlink(user.full_name, f"tg://user?id={user.id}"):
                token.holders.get(userfriendly_to_raw(user.wallet_address), 0)
            for user in users if
            user.wallet_address and token.holders.get(userfriendly_to_raw(user.wallet_address), 0) > 0
        }
        sorted_holders = sorted(top_holders.items(), key=lambda item: item[1], reverse=True)

        items_per_page = 10
        start_index = (page - 1) * items_per_page
        paginated_holders = sorted_holders[start_index:start_index + items_per_page]

        top_holders_text = "\n".join(
            f"{rank + start_index + 1}. {full_name}: {hcode(amount_str(balance))}"
            for rank, (full_name, balance) in enumerate(paginated_holders)
        )

        total_pages = (len(sorted_holders) + items_per_page - 1) // items_per_page
        text = manager.text_message.get("top_holders").format(top_holders=top_holders_text)
        paginator = InlineKeyboardPaginator(None, page, total_pages, str(token.id) + ":{}")

        message_answer = message.reply if send_mode == SendMode.SEND else message.edit_text
        await message_answer(text, reply_markup=paginator.as_markup())
