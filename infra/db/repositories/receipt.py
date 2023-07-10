import logging
from datetime import datetime
from sqlalchemy import select, update, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, contains_eager

from domain.entities.receipt import ReceiptItem, Receipt
from domain.interfaces.repositories.receipts import IReceiptRepo
from infra.db.models.receipt import ReceiptModel, ReceiptItemModel, ReceiptLabelsModel
from infra.db.ctx import db_ctx, ReadOnlyCtx


def item_to_entity(item: ReceiptItemModel) -> ReceiptItem:
    return ReceiptItem(
        id=item.id,
        amount=item.amount,
        name=item.name,
        qty=item.qty
    )


def model_to_entity(model: ReceiptModel) -> Receipt:
    receipt = Receipt(
        id=model.id,
        amount=model.amount,
        description=model.description,
        budget_id=model.budget_id,
        date=model.date,
        items=[item_to_entity(item) for item in model.items],
        labels=[label.name for label in model.labels]
    )
    return receipt


def entity_to_model(receipt: Receipt, new: bool = True) -> ReceiptModel:
    receipt_model = ReceiptModel(
        id=receipt.id if not new else None,
        amount=receipt.amount,
        fact_amount=receipt.fact_amount,
        description=receipt.description,
        budget_id=receipt.budget_id,
        date=receipt.date,
        deleted_at=None,
        items=entity_to_items_model(receipt=receipt, new=new),
        labels=entity_to_receipt_labels_model(receipt=receipt, new=new)
    )
    return receipt_model


def entity_to_items_model(
        receipt: Receipt,
        new: bool = False
) -> list[ReceiptItemModel]:
    return [
        ReceiptItemModel(
            id=item.id,
            amount=item.amount,
            qty=item.qty,
            name=item.name,
            receipt_id=receipt.id if not new else None
        )
        for item in receipt.items
    ]


def entity_to_receipt_labels_model(
        receipt: Receipt,
        new: bool = False
) -> list[ReceiptLabelsModel]:
    return [
        ReceiptLabelsModel(
            name=label,
            receipt_id=receipt.id if not new else None
        )
        for label in receipt.labels
    ]


class ReceiptRepo(IReceiptRepo):

    def __init__(self, ctx: ReadOnlyCtx[AsyncSession]) -> None:
        self._ctx = ctx

    @property
    def ctx(self) -> AsyncSession:
        return self._ctx.get()

    async def get(self, id: int, budget_id: str) -> Receipt | None:
        receipt_stmt = select(ReceiptModel).options(
            selectinload(ReceiptModel.labels), selectinload(ReceiptModel.items)
        ).where(
            ReceiptModel.id == id,
            ReceiptModel.budget_id == budget_id,
            ReceiptModel.deleted_at.is_(None)
        )
        receipt = await self.ctx.scalar(receipt_stmt)
        if not receipt:
            return None
        return model_to_entity(receipt)

    async def list_(
            self,
            budget_id: str,
            labels: list[str],
            date_from: datetime | None = None,
            date_to: datetime | None = None
    ) -> list[Receipt]:
        stmt = select(ReceiptModel).join(ReceiptModel.labels).options(
            contains_eager(ReceiptModel.labels), selectinload(ReceiptModel.items))
        where_clause = [
            ReceiptModel.budget_id == budget_id,
            ReceiptModel.deleted_at.is_(None)
        ]
        logging.warning(f'check query {labels}, {date_from}, {date_to}')
        if labels:
            where_clause.append(ReceiptModel.labels.any(ReceiptLabelsModel.name.in_(labels)))
        if date_from:
            where_clause.append(ReceiptModel.date > date_from)
        if date_to:
            where_clause.append(ReceiptModel.date < date_to)

        stmt = stmt.where(*where_clause)
        data = await self.ctx.scalars(stmt)
        return [model_to_entity(model=receipt) for receipt in data.unique()]

    async def label_list(self, budget_id: str) -> list[str]:
        stmt = (
            select(ReceiptLabelsModel.name)
            .join(ReceiptModel)
            .where(ReceiptModel.budget_id == budget_id)
            .distinct(ReceiptLabelsModel.name)
        )
        items: ScalarResult[str] = await self.ctx.scalars(stmt)
        return items.all()

    async def add(self, receipt: Receipt) -> Receipt:
        receipt_model = entity_to_model(receipt, new=True)
        self.ctx.add(receipt_model)
        await self.ctx.flush()
        return model_to_entity(receipt_model)

    async def update(self, budget_id: str, receipt_id: str):
        # option 1
        #   - add version to receipt,
        #   FK or join to version,
        #   up ver - receipt and insert new
        #   set deleted at on previous version
        pass

    async def delete(self, budget_id, receipt_id) -> int:
        stmt = (
            update(ReceiptModel)
            .where(ReceiptModel.budget_id == budget_id, ReceiptModel.id == receipt_id)
            .values({'deleted_at': datetime.now()})
            .returning(ReceiptModel.id)
        )
        return await self.ctx.scalar(stmt)


repo = ReceiptRepo(db_ctx)
