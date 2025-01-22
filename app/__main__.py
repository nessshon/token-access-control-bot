import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_tonconnect.tonconnect.storage import ATCRedisStorage
from pytonapi import AsyncTonapi
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from tonutils.tonconnect import TonConnect

from .bot.commands import (
    bot_commands_setup,
    bot_commands_delete,
    bot_admin_commands_setup,
    bot_admin_commands_delete,
)
from .bot.handlers import bot_routers_include
from .bot.middlewares import bot_middlewares_register
from .config import Config, load_config
from .db.models import Base, AdminDB
from .logger import setup_logger
from .scheduler import Scheduler


async def on_startup(
        dispatcher: Dispatcher,
        bot: Bot,
        config: Config,
        tonapi: AsyncTonapi,
        redis: Redis,
        scheduler: Scheduler,
        engine: AsyncEngine,
        sessionmaker: async_sessionmaker,
        tonconnect: TonConnect,
) -> None:
    """
    Startup event handler. This runs when the bot starts up.
    """
    loop = asyncio.get_event_loop()
    loop.__setattr__("dispatcher", dispatcher)
    loop.__setattr__("bot", bot)
    loop.__setattr__("config", config)
    loop.__setattr__("tonapi", tonapi)
    loop.__setattr__("tonconnect", tonconnect)
    loop.__setattr__("sessionmaker", sessionmaker)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot_middlewares_register(
        dispatcher,
        redis=redis,
        config=config,
        scheduler=scheduler,
        sessionmaker=sessionmaker,
        tonconnect=tonconnect,
    )
    bot_routers_include(dispatcher)
    scheduler.run()

    admins_ids = await AdminDB.get_all_ids(sessionmaker, config)
    await bot_commands_setup(bot)
    await bot_admin_commands_setup(bot, admins_ids)


async def on_shutdown(
        bot: Bot,
        config: Config,
        scheduler: Scheduler,
        engine: AsyncEngine,
        sessionmaker: async_sessionmaker,
) -> None:
    """
    Shutdown event handler. This runs when the bot shuts down.
    """
    admins_ids = await AdminDB.get_all_ids(sessionmaker, config)

    await bot_commands_delete(bot)
    await bot_admin_commands_delete(bot, admins_ids)
    await bot.delete_webhook()
    await bot.session.close()
    await engine.dispose()
    scheduler.shutdown()


async def main() -> None:
    """
    Main function that initializes the bot and starts the event loop.
    """
    config = load_config()

    scheduler = Scheduler(config=config)

    tonapi = AsyncTonapi(
        config.tonapi.KEY,
        is_testnet=config.IS_TESTNET,
        max_retries=5,
    )

    engine = create_async_engine(
        config.database.dsn(),
        pool_pre_ping=True,
    )
    sessionmaker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    storage = RedisStorage.from_url(
        url=config.redis.dsn(),
    )
    tonconnect = TonConnect(
        storage=ATCRedisStorage(storage.redis),
        manifest_url=config.MANIFEST_URL,
        api_tokens={"tonapi": config.tonapi.TONCONNECT_KEY},
    )
    bot = Bot(
        token=config.bot.TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )
    dp = Dispatcher(
        bot=bot,
        storage=storage,
        config=config,
        redis=storage.redis,
        engine=engine,
        sessionmaker=sessionmaker,
        scheduler=scheduler,
        tonapi=tonapi,
        tonconnect=tonconnect,
    )

    # Register startup handler
    dp.startup.register(on_startup)
    # Register shutdown handler
    dp.shutdown.register(on_shutdown)

    # Start the bot
    await bot.delete_webhook()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # Setup logging
    setup_logger(logging.DEBUG)
    # Run the bot
    asyncio.run(main())
