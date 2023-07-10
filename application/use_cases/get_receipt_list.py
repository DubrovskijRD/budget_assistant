from datetime import datetime
from application.unit_of_work import IUoW
from domain.entities.receipt import Receipt


class UseCase:
    def __init__(self, uow: IUoW):
        self._uow = uow

    async def execute(
            self,
            budget_id: str,
            labels: list[str],
            date_from: datetime | None,
            date_to: datetime | None
    ) -> list[Receipt]:
        async with self._uow as uow:
            res = await uow.receipts.list_(
                budget_id=budget_id,
                labels=labels,
                date_from=date_from,
                date_to=date_to
            )
            return res
