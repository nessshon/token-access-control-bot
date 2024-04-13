from typing import Dict

from aiogram_tonconnect.utils.texts import TextMessage as AiogramTonconnectTextMessageBase

from ...texts import (
    SUPPORTED_LANGUAGES,

    TEXT_MESSAGES,
    TEXT_BUTTONS,
)


class AiogramTonconnectTextMessage(AiogramTonconnectTextMessageBase):

    @property
    def texts_messages(self) -> Dict[str, Dict[str, str]]:
        return TEXT_MESSAGES


class TextButton:
    """
    Subclass of Text for managing text buttons in different languages.
    """

    def __init__(self, language_code: str) -> None:
        """
        Initializes the Text instance with the specified language code.

        :param language_code: The language code (e.g., "ru" or "en").
        """
        self.language_code = language_code if language_code in SUPPORTED_LANGUAGES.keys() else "en"

    def get(self, code: str) -> str:
        """
        Retrieves the text corresponding to the provided code in the current language.

        :param code: The code associated with the desired text.
        :return: The text in the current language.
        """
        return TEXT_BUTTONS[self.language_code][code]


class TextMessage:
    """
    Subclass of Text for managing text messages in different languages.
    """

    def __init__(self, language_code: str) -> None:
        """
        Initializes the Text instance with the specified language code.

        :param language_code: The language code (e.g., "ru" or "en").
        """
        self.language_code = language_code if language_code in SUPPORTED_LANGUAGES.keys() else "en"

    def get(self, code: str) -> str:
        """
        Retrieves the text corresponding to the provided code in the current language.

        :param code: The code associated with the desired text.
        :return: The text in the current language.
        """
        return TEXT_MESSAGES[self.language_code][code]
