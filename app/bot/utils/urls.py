from aiogram.utils.markdown import hlink


class BaseUrl:

    def __init__(self, base_url: str, address: str, name: str = None) -> None:
        self.base_url = base_url
        self.address = address
        self.name = name

    @property
    def link(self) -> str:
        return f"{self.base_url}/{self.address}"

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
    BASE_URL = "https://tonviewer.com"

    def __init__(self, address: str, name: str = None) -> None:
        super().__init__(self.BASE_URL, address, name)


class GetgemsUrl(BaseUrl):
    BASE_URL = "https://gegtems.com/collection"

    def __init__(self, address: str, name: str = None) -> None:
        super().__init__(self.BASE_URL, address, name)


class DeDustUrl(BaseUrl):
    BASE_URL = "https://dedust.io/swap/TON"

    def __init__(self, address: str, name: str = None) -> None:
        super().__init__(self.BASE_URL, address, name)
