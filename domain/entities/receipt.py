from datetime import datetime
from dataclasses import dataclass
from domain.vo.amount import Amount


@dataclass
class ReceiptItem:
    id: int | None
    name: str
    amount: Amount
    qty: int

    @property
    def total_amount(self):
        return self.amount * self.qty


class Receipt:
    def __init__(
            self,
            id: int | None,
            budget_id: str,
            amount: Amount,
            description: str | None,
            labels: list[str],
            items: list[ReceiptItem],
            date: datetime
    ):
        self._id = id
        self._budget_id = budget_id
        self._amount = amount
        self._description = description
        self._labels = labels  # food, tech, med, utility, transport, house, clothes
        self._items: list[ReceiptItem] = []
        self._date = date
        self._fact_amount = Amount(0)
        for item in items:
            self.add_item(item)

    @classmethod
    def new(
            cls,
            budget_id: str,
            amount: Amount,
            description: str | None,
            labels: list[str],
            items: list[ReceiptItem],
            date: datetime
    ):
        return cls(
            id=None,
            budget_id=budget_id,
            amount=amount,
            description=description,
            labels=labels,
            items=items,
            date=date
        )

    @property
    def items(self) -> tuple[ReceiptItem]:
        return tuple(self._items)

    @property
    def id(self) -> int:
        if self._id is None:
            raise TypeError("Entity state invalid")
        return self._id

    @property
    def budget_id(self) -> str:
        return self._budget_id

    @property
    def amount(self) -> Amount:
        return self._amount

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def fact_amount(self) -> Amount:
        return self._fact_amount

    @property
    def labels(self) -> list[str]:
        return self._labels

    @property
    def date(self) -> datetime:
        return self._date

    def add_item(self, item: ReceiptItem) -> None:
        updated_fact_amount = self._fact_amount + item.total_amount
        if self.amount < updated_fact_amount:
            raise ValueError(
                f'Invalid receipt amount: {self.amount} < {updated_fact_amount}'
            )
        self._fact_amount = updated_fact_amount
        self._items.append(item)

