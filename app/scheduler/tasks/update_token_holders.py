import asyncio
import logging

from aiogram import Bot
from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIInternalServerError
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
                collection = await tonapi.nft.get_collection_by_collection_address(account_id=token.address)
                total_holders, found_holders = collection.next_item_index, 0

                for nft in request.nft_items:
                    if nft.owner.address.to_raw() in holders:
                        holders[nft.owner.address.to_raw()] += 1
                    else:
                        holders[nft.owner.address.to_raw()] = 1
                    found_holders += 1

            else:
                request = await tonapi.jettons.get_all_holders(account_id=token.address)
                total_holders, found_holders = request.total, 0

                for address in request.addresses:
                    holders[address.owner.address.to_raw()] = nano_to_amount(int(address.balance), 9)
                    found_holders += 1

        except TONAPIInternalServerError as e:
            logging.error(f"{e.__class__.__name__}: {e}")
            logging.error(f"Failed to update holders for {token.name} [{token.address}]")
            continue

        except Exception as e:
            await send_message(bot, config.bot.DEV_ID, text=f"{e.__class__.__name__}: {e}")
            logging.error(f"{e.__class__.__name__}: {e}")
            logging.error(f"Failed to update holders for {token.name} [{token.address}]")
            continue

        if holders and total_holders == found_holders:
            await TokenDB.update(sessionmaker, primary_key=token.id, holders=holders)
        else:
            logging.error(f"Failed to update holders for {token.name} [{token.address}]")
            logging.error(f"Found holders: {found_holders}, Total Holders: {total_holders}")
