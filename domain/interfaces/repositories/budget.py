from abc import ABC, abstractmethod


class IBudgetRepo(ABC):

    @abstractmethod
    async def add(self, id: str) -> None:
        pass
