from __future__ import annotations

from sqlalchemy import *

from ._abc import AbstractModel


class TokenDB(AbstractModel):
    __tablename__ = "tokens"

    class Type:
        NFTCollection = "nft_collection"
        JettonMaster = "jetton_master"

        @classmethod
        def values(cls) -> list[str]:
            return [cls.NFTCollection, cls.JettonMaster]

    id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    type = Column(
        VARCHAR(length=32),
        nullable=False,
    )
    address = Column(
        VARCHAR(length=48),
        nullable=False,
    )
    holders = Column(
        JSON,
        nullable=True,
    )
    min_amount = Column(
        BigInteger,
        nullable=False,
        default=0,
    )
    decimals = Column(
        Integer,
        nullable=True,
        default=9,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
