from contextvars import ContextVar
from typing import Protocol, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

ctx: ContextVar[AsyncSession | None] = ContextVar('db_ctx', default=None)

X = TypeVar('X')


class ReadOnlyCtx(Protocol[X]):
    def get(self) -> X:
        pass


db_ctx: ReadOnlyCtx[AsyncSession] = ctx
