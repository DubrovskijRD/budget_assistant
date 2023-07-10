from abc import ABC, abstractmethod
from datetime import datetime

from domain.entities.receipt import Receipt


class IReceiptRepo(ABC):

    @abstractmethod
    async def get(self, id: int, budget_id: str) -> Receipt | None:
        pass

    @abstractmethod
    async def list_(
            self,
            budget_id: str,
            labels: list[str],
            date_from: datetime | None = None,
            date_to: datetime | None = None
    ) -> list[Receipt]:
        pass

    @abstractmethod
    async def label_list(self, budget_id: str) -> list[str]:
        pass

    @abstractmethod
    async def add(self, receipt: Receipt) -> Receipt:
        pass

    @abstractmethod
    async def delete(self, budget_id, receipt_id) -> str:
        pass
