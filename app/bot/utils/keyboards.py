from typing import Dict, Optional, Sequence, List, Tuple

from aiogram.types import InlineKeyboardButton as Button
from aiogram.types import InlineKeyboardMarkup as Markup
from aiogram.utils.keyboard import InlineKeyboardBuilder as Builder
from aiogram_tonconnect.utils.keyboards import InlineKeyboard as AiogramTonconnectInlineKeyboardBase

from .texts import TextButton
from .urls import NFTBuyUrl, JettonBuyUrl
from ...db.models import ChatDB, TokenDB
from ...texts import TEXT_BUTTONS, SUPPORTED_LANGUAGES


class AiogramTonconnectInlineKeyboard(AiogramTonconnectInlineKeyboardBase):

    @property
    def texts_buttons(self) -> Dict[str, Dict[str, str]]:
        return TEXT_BUTTONS


def back(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("back"), callback_data="back")],
        ]
    )


def main(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("main"), callback_data="main")],
        ]
    )


def select_language() -> Markup:
    builder = Builder().row(
        *[
            Button(text=text, callback_data=callback_data)
            for callback_data, text in SUPPORTED_LANGUAGES.items()
        ], width=3
    )
    return builder.as_markup()


def main_menu(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("get_access"), callback_data="get_access")],
            [Button(text=text_button.get("change_language"), callback_data="change_language"),
             Button(text=text_button.get("disconnect_wallet"), callback_data="disconnect_wallet")],
        ]
    )


def allow_access(text_button: TextButton, chats: Sequence[ChatDB]) -> Markup:
    inline_keyboard = []
    for chat in chats:
        inline_keyboard.append([Button(text=f"💬 {chat.name}", url=chat.invite_link)])
    inline_keyboard.append([Button(text=text_button.get("main"), callback_data="main")])

    return Markup(inline_keyboard=inline_keyboard)


def deny_access(text_button: TextButton, tokens: Sequence[TokenDB]) -> Markup:
    inline_keyboard = []
    for token in tokens:
        if token.type == TokenDB.Type.NFTCollection:
            url = NFTBuyUrl(token.address).link
            text = f"🖼 {token.name}"
        else:
            url = JettonBuyUrl(token.address).link
            text = f"🪙 {token.name}"
        inline_keyboard.append([Button(text=text, url=url)])
    inline_keyboard.append([Button(text=text_button.get("main"), callback_data="main")])

    return Markup(inline_keyboard=inline_keyboard)


def select_tokens(tokens: Sequence[TokenDB]) -> Markup:
    builder = Builder()
    builder.row(
        *[
            Button(text=token.name, callback_data=f"{token.id}:{1}")
            for token in tokens
        ], width=1,
    )

    return builder.as_markup()


class InlineKeyboardPaginator:
    """
    A class that generates an inline keyboard for paginated data.

    Args:
        items (List[Tuple]): A list of tuples containing the data to be displayed in the keyboard.
        total_pages (int): The total number of pages.
        current_page (int): The current page number.
        data_pattern (str): The pattern to be used for the callback data.
        before_reply_markup (InlineKeyboardMarkup): A builder to be attached before the items and navigation.
        after_reply_markup (InlineKeyboardMarkup): A builder to be attached after the items and navigation.
    """

    first_page_label = "« {}"
    previous_page_label = "‹ {}"
    current_page_label = "· {} ·"
    next_page_label = "{} ›"
    last_page_label = "{} »"

    def __init__(
            self,
            items: Optional[List[Tuple]] = None,
            current_page: int = 1,
            total_pages: int = 1,
            data_pattern: str = "page:{}",
            before_reply_markup: Optional[Markup] = None,
            after_reply_markup: Optional[Markup] = None,
    ) -> None:
        self.items = items or []
        self.current_page = current_page
        self.total_pages = total_pages
        self.data_pattern = data_pattern

        self.builder = Builder()
        self.before_reply_markup = before_reply_markup
        self.after_reply_markup = after_reply_markup

    def _items_builder(self) -> Builder:
        builder = Builder()

        for key, val in self.items:
            builder.button(text=str(key), callback_data=str(val))
        builder.adjust(1)

        return builder

    def _navigation_builder(self) -> Builder:
        builder = Builder()
        keyboard_dict = {}

        if self.total_pages > 1:
            if self.total_pages <= 5:
                for page in range(1, self.total_pages + 1):
                    keyboard_dict[page] = page
            else:
                if self.current_page <= 3:
                    page_range = range(1, 4)
                    keyboard_dict[4] = self.next_page_label.format(4)
                    keyboard_dict[self.total_pages] = self.last_page_label.format(self.total_pages)
                elif self.current_page > self.total_pages - 3:
                    keyboard_dict[1] = self.first_page_label.format(1)
                    keyboard_dict[self.total_pages - 3] = self.previous_page_label.format(self.total_pages - 3)
                    page_range = range(self.total_pages - 2, self.total_pages + 1)
                else:
                    keyboard_dict[1] = self.first_page_label.format(1)
                    keyboard_dict[self.current_page - 1] = self.previous_page_label.format(self.current_page - 1)
                    keyboard_dict[self.current_page + 1] = self.next_page_label.format(self.current_page + 1)
                    keyboard_dict[self.total_pages] = self.last_page_label.format(self.total_pages)
                    page_range = [self.current_page]
                for page in page_range:
                    keyboard_dict[page] = page
            keyboard_dict[self.current_page] = self.current_page_label.format(self.current_page)

            for key, val in sorted(keyboard_dict.items()):
                builder.button(text=str(val), callback_data=str(self.data_pattern.format(key)))
            builder.adjust(5)

        return builder

    def as_markup(self) -> Markup:
        if self.before_reply_markup:
            self.builder.attach(Builder(markup=self.before_reply_markup.inline_keyboard))

        self.builder.attach(self._items_builder())
        self.builder.attach(self._navigation_builder())

        if self.after_reply_markup:
            self.builder.attach(Builder(markup=self.after_reply_markup.inline_keyboard))

        return self.builder.as_markup()


def back_add(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("back"), callback_data="back"),
             Button(text=text_button.get("add"), callback_data="add")],
        ]
    )


def back_delete(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("back"), callback_data="back"),
             Button(text=text_button.get("delete"), callback_data="delete")],
        ]
    )


def back_confirm(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("back"), callback_data="back"),
             Button(text=text_button.get("confirm"), callback_data="confirm")],
        ]
    )


def admin_menu(text_button: TextButton) -> Markup:
    return Markup(
        inline_keyboard=[
            [Button(text=text_button.get("admins_menu"), callback_data="admins_menu")],
            [Button(text=text_button.get("chats_menu"), callback_data="chats_menu"),
             Button(text=text_button.get("tokens_menu"), callback_data="tokens_menu")],
            [Button(text=text_button.get("newsletter"), callback_data="newsletter")],
            [Button(text=text_button.get("main"), callback_data="main")],
        ]
    )


def token_info(text_button: TextButton) -> Markup:
    inline_keyboard = [
        [Button(text=text_button.get("edit_min_amount"), callback_data="edit_min_amount")]
    ]
    return Markup(inline_keyboard=inline_keyboard + back_delete(text_button).inline_keyboard)
