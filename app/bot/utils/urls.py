import asyncio

from aiogram.utils.markdown import hlink

from app.config import Config


class BaseUrl:

    def __init__(self, base_url: str, address: str, name: str = None) -> None:
        self.base_url = base_url
        self.address = address
        self.name = name

    @property
    def link(self) -> str:
        return f"{self.base_url}{self.address}"

    @property
    def hlink(self) -> str:
        return hlink(title=self.address, url=self.link)

    @property
    def hlink_short(self) -> str:
        return hlink(title=f"{self.address[:4]}...{self.address[-4:]}", url=self.link)

    @property
    def hlink_name(self) -> str:
        return hlink(title=self.name, url=self.link)


class TonviewerUrl(BaseUrl):
    BASE_URL = "https://tonviewer.com/"

    def __init__(self, address: str, name: str = None) -> None:
        super().__init__(self.BASE_URL, address, name)


class NFTBuyUrl(BaseUrl):
    BASE_URL = "https://getgems.io/collection/"

    def __init__(self, address: str, name: str = None) -> None:
        super().__init__(self.BASE_URL, address, name)


class JettonBuyUrl(BaseUrl):
    DEDUST_BASE_URL = "https://dedust.io/swap/TON/"
    STONFI_BASE_URL = "https://app.ston.fi/swap?chartVisible=false&ft=TON&tt="
    SWAPCOFFEE_BASE_URL = "https://swap.coffee/dex?ft=TON&st="

    def __init__(self, address: str, name: str = None) -> None:
        loop = asyncio.get_running_loop()
        config: Config = getattr(loop, "config")

        if config.DEX_NAME == "dedust":
            super().__init__(self.DEDUST_BASE_URL, address, name)
        elif config.DEX_NAME == "stonfi":
            super().__init__(self.STONFI_BASE_URL, address, name)
        elif config.DEX_NAME == "swapcoffee":
            super().__init__(self.SWAPCOFFEE_BASE_URL, address, name)

        else:
            raise ValueError(f"Unsupported dex: {config.DEX_NAME}")
