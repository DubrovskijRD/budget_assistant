from application.unit_of_work import IUoW
from domain.entities.receipt import Receipt


class UseCase:
    def __init__(self, uow: IUoW):
        self._uow = uow

    async def execute(self, receipt: Receipt) -> Receipt:
        async with self._uow as uow:
            new_receipt = await uow.receipts.add(receipt=receipt)
            await uow.commit()
        return new_receipt
