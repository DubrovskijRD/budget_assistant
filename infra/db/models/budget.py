from datetime import datetime
from ipaddress import IPv4Address
from sqlalchemy import DateTime, text, func

from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class BudgetModel(Base):
    __tablename__ = 'budgets'
    id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), default=None
    )


class BudgetEventModel(Base):
    __tablename__ = 'budget_events'

    action: Mapped[str]
    user_ip: Mapped[IPv4Address] = mapped_column(INET)
    budget_id: Mapped[str] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        primary_key=True,
        server_default=func.now(),
        default=None
    )
