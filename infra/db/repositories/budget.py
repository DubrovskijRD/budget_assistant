from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.repositories.budget import IBudgetRepo
from infra.db.models.budget import BudgetModel
from infra.db.ctx import db_ctx, ReadOnlyCtx


class BudgetRepo(IBudgetRepo):

    def __init__(self, ctx: ReadOnlyCtx[AsyncSession]) -> None:
        self._ctx = ctx

    def set_ctx(self, ctx: ReadOnlyCtx[AsyncSession]):
        self._ctx = ctx

    @property
    def ctx(self) -> AsyncSession:
        return self._ctx.get()

    async def add(self, id: str) -> None:
        obj = BudgetModel(id=id)
        self.ctx.add(obj)
        await self.ctx.flush()


repo = BudgetRepo(db_ctx)
