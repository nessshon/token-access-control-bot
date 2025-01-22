import os
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import environs
from environs import Env

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class BotConfig:
    TOKEN: str
    DEV_ID: int
    ADMIN_ID: int


@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB: int

    def dsn(self) -> str:
        """
        Generates a Redis connection DSN (Data Source Name) using the provided host, port, and database.

        :return: The generated DSN.
        """
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


@dataclass
class DatabaseConfig:
    PATH: str
    FILENAME: str

    def dsn(self) -> str:
        """
        Generates a SQLite connection DSN (Data Source Name) using the provided filename.

        :return: The generated DSN.
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)
        return f"sqlite+aiosqlite:///{self.PATH}/{self.FILENAME}"


@dataclass
class TONAPIConfig:
    KEY: str
    RPS: int
    TONCONNECT_KEY: Union[str, None]


@dataclass
class SchedulerConfig:
    CHECK_CHAT_MEMBERS_INTERVAL: int
    UPDATE_TOKEN_HOLDERS_INTERVAL: int


@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    database: DatabaseConfig
    tonapi: TONAPIConfig
    scheduler: SchedulerConfig

    DEX_NAME: str
    IS_TESTNET: bool
    MANIFEST_URL: str


def load_config() -> Config:
    env = Env()
    env.read_env()

    try:
        tonconnect_key = env.str("TONAPI_TONCONNECT_KEY", None)
    except environs.EnvValidationError:
        tonconnect_key = None

    return Config(
        bot=BotConfig(
            TOKEN=env.str("BOT_TOKEN"),
            DEV_ID=env.int("BOT_DEV_ID"),
            ADMIN_ID=env.int("BOT_ADMIN_ID"),
        ),
        redis=RedisConfig(
            HOST=env.str("REDIS_HOST"),
            PORT=env.int("REDIS_PORT"),
            DB=env.int("REDIS_DB"),
        ),
        database=DatabaseConfig(
            PATH=f"{BASE_DIR}/db/data",
            FILENAME="database.sqlite",
        ),
        tonapi=TONAPIConfig(
            KEY=env.str("TONAPI_KEY"),
            RPS=env.int("TONAPI_RPS"),
            TONCONNECT_KEY=tonconnect_key,
        ),
        scheduler=SchedulerConfig(
            CHECK_CHAT_MEMBERS_INTERVAL=env.int("SCHEDULER_CHECK_CHAT_MEMBERS_INTERVAL"),
            UPDATE_TOKEN_HOLDERS_INTERVAL=env.int("SCHEDULER_UPDATE_TOKEN_HOLDERS_INTERVAL"),
        ),

        DEX_NAME=env.str("DEX_NAME"),
        IS_TESTNET=env.bool("IS_TESTNET"),
        MANIFEST_URL=env.str("MANIFEST_URL"),
    )
