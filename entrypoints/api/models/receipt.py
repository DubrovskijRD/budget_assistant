from datetime import datetime
from typing import Annotated
import msgspec
from msgspec import Struct

from domain.entities.receipt import Receipt, ReceiptItem
from domain.vo.amount import Amount

IAmount = Annotated[float, msgspec.Meta(gt=0)]
DtWithoutTz = Annotated[datetime, msgspec.Meta(tz=False)]


class ReceiptItemCreateStruct(Struct):
    name: str
    amount: IAmount
    qty: int

    def to_entity(self) -> ReceiptItem:
        return ReceiptItem(
            id=None,
            name=self.name,
            qty=self.qty,
            amount=Amount(self.amount)
        )


class ReceiptCreateStruct(Struct):
    amount: IAmount
    labels: list[str]
    description: str | None
    date: DtWithoutTz
    items: list[ReceiptItemCreateStruct] = []

    def to_entity(self, budget_id) -> Receipt:
        return Receipt.new(
            budget_id=budget_id,
            amount=Amount(self.amount),
            description=self.description,
            date=self.date,
            labels=self.labels,
            items=[item.to_entity() for item in self.items]
        )


class ReceiptItemStruct(Struct):
    id: int
    name: str
    amount: IAmount
    qty: int

    @classmethod
    def from_entity(cls, entity: ReceiptItem) -> 'ReceiptItemStruct':
        return ReceiptItemStruct(
            id=entity.id,
            name=entity.name,
            amount=float(entity.amount),
            qty=entity.qty
        )


class ReceiptStruct(Struct):
    id: str
    budget_id: str
    amount: IAmount
    fact_amount: IAmount
    description: str | None
    labels: list[str]
    date: DtWithoutTz
    items: list[ReceiptItemStruct] = []

    @classmethod
    def from_entity(cls, entity: Receipt) -> 'ReceiptStruct':
        return ReceiptStruct(
            id=entity.id,
            budget_id=entity.budget_id,
            amount=float(entity.amount),
            description=entity.description,
            fact_amount=float(entity.fact_amount),
            labels=entity.labels,
            date=entity.date,
            items=[ReceiptItemStruct.from_entity(item) for item in entity.items]
        )
