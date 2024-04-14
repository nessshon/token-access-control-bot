import asyncio

from pytonapi import AsyncTonapi
from pytonapi.utils import nano_to_amount
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.models import TokenDB


async def update_token_holders() -> None:
    loop = asyncio.get_event_loop()
    tonapi: AsyncTonapi = loop.__getattribute__("tonapi")
    sessionmaker: async_sessionmaker = loop.__getattribute__("sessionmaker")

    tokens = await TokenDB.all(sessionmaker)
    for token in tokens:
        holders = {}
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
                holders[address.owner.address.to_raw()] = nano_to_amount(int(address.balance))

        await TokenDB.update(sessionmaker, primary_key=token.id, holders=holders)
