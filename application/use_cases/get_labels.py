from application.unit_of_work import IUoW


class UseCase:
    def __init__(self, uow: IUoW):
        self._uow = uow

    async def execute(self, budget_id: str) -> list[str]:
        async with self._uow as uow:
            ret = await uow.receipts.label_list(budget_id=budget_id)
            return ret
