import asyncio

from aiogram import Bot
from pytonapi import AsyncTonapi
from pytonapi.utils import nano_to_amount
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.utils.messages import send_message
from app.config import Config
from app.db.models import TokenDB


async def update_token_holders() -> None:
    loop = asyncio.get_event_loop()
    bot: Bot = loop.__getattribute__("bot")
    config: Config = loop.__getattribute__("config")
    tonapi: AsyncTonapi = loop.__getattribute__("tonapi")
    sessionmaker: async_sessionmaker = loop.__getattribute__("sessionmaker")

    tokens = await TokenDB.all(sessionmaker)
    for token in tokens:
        holders = {}
        try:
            if token.type == TokenDB.Type.NFTCollection:
                request = await tonapi.nft.get_all_items_by_collection_address(account_id=token.address)
                for nft in request.nft_items:
                    if nft.owner.address.to_raw() in holders:
                        holders[nft.owner.address.to_raw()] += 1
                    else:
                        holders[nft.owner.address.to_raw()] = 1
            else:
                request = await tonapi.jettons.get_all_holders(account_id=token.address)
                for address in request.addresses:
                    holders[address.owner.address.to_raw()] = nano_to_amount(int(address.balance), 9)

        except Exception as e:
            await send_message(bot, config.bot.DEV_ID, text=f"{e.__class__.__name__}: {e}")
            continue

        if holders:
            await TokenDB.update(sessionmaker, primary_key=token.id, holders=holders)
