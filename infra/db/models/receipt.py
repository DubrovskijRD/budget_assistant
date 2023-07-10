from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from domain.vo.amount import Amount


class ReceiptLabelsModel(Base):
    __tablename__ = 'receipt_labels'
    name: Mapped[str] = mapped_column(primary_key=True)
    receipt_id: Mapped[int] = mapped_column(ForeignKey('receipts.id'), primary_key=True)


class ReceiptItemModel(Base):
    __tablename__ = 'receipt_items'
    id: Mapped[int] = mapped_column(
        Sequence('receipt_items_id', start=2000000, increment=2),
        primary_key=True
    )
    receipt_id: Mapped[int] = mapped_column(ForeignKey('receipts.id'))
    name: Mapped[str]
    amount: Mapped[Amount]
    qty: Mapped[int]


class ReceiptModel(Base):
    __tablename__ = 'receipts'
    id: Mapped[int] = mapped_column(
        Sequence('receipts_id', start=10000, increment=3),
        primary_key=True
    )
    budget_id: Mapped[str] = mapped_column(ForeignKey('budgets.id'))
    amount: Mapped[Amount]
    description: Mapped[str | None]
    fact_amount: Mapped[Amount]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    labels: Mapped[list[ReceiptLabelsModel]] = relationship("ReceiptLabelsModel")
    items: Mapped[list[ReceiptItemModel]] = relationship("ReceiptItemModel")
