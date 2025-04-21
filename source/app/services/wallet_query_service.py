from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import WalletQuery
from app.exceptions import PageIndexException


class WalletQueryService:
    def __init__(self,
                 factory_session: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.factory_session = factory_session

    async def insert_wallet_access(self,
                                   addr: str,
                                   bandwidth: int,
                                   energy: int,
                                   balance: float) -> WalletQuery:
        async with self.factory_session() as session:
            entity = WalletQuery(
                address=addr,
                bandwidth=bandwidth,
                energy=energy,
                balance=balance)

            try:
                session.add(entity)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return entity

    async def select_wallet_queries(self, page: int, per_page: int) -> Sequence[WalletQuery]:
        async with self.factory_session() as session:
            query = (
                select(WalletQuery)
                .order_by(WalletQuery.created_at.desc())
                .limit(per_page)
                .offset((page - 1) * per_page)
            )

            execution = await session.execute(query)
            entities = (execution
                        .scalars()
                        .all())

            if not entities:
                raise PageIndexException(page, per_page)

            return entities

    async def total_counts(self) -> int:
        async with self.factory_session() as session:
            query = (
                select(func.count())
                .select_from(WalletQuery)
            )
            total = await session.scalar(query)
            if not total:
                raise ValueError
            return total
