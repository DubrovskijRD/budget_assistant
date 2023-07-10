from abc import ABC, abstractmethod
from domain.interfaces.repositories.budget import IBudgetRepo
from domain.interfaces.repositories.receipts import IReceiptRepo


class IUoW(ABC):

    @abstractmethod
    async def __aenter__(self) -> 'IUoW':
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @property
    @abstractmethod
    def receipts(self) -> IReceiptRepo:
        pass

    @property
    @abstractmethod
    def budgets(self) -> IBudgetRepo:
        pass
