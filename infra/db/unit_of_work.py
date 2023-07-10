from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from .ctx import ctx
from application.unit_of_work import IUoW
from infra.db.repositories.receipt import repo as receipt_repo, ReceiptRepo
from infra.db.repositories.budget import repo as budget_repo, BudgetRepo


class UoW(IUoW):

    def __init__(self, session_factory: sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._sess: AsyncSession | None = None

    async def __aenter__(self) -> 'UoW':
        self._sess = self._session_factory()
        ctx.set(self._sess)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ctx.set(None)
        await self._sess.rollback()
        await self._sess.close()

    async def commit(self) -> None:
        await self._sess.commit()

    async def rollback(self) -> None:
        await self._sess.rollback()

    @property
    def receipts(self) -> ReceiptRepo:
        return receipt_repo

    @property
    def budgets(self) -> BudgetRepo:
        return budget_repo
