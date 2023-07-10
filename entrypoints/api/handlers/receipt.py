import logging
from datetime import datetime
from dataclasses import dataclass
from aiohttp.web import HTTPNotFound
from mashumaro.mixins.dict import DataClassDictMixin
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.unit_of_work import UoW
from entrypoints.api.models.receipt import ReceiptStruct, ReceiptCreateStruct
from entrypoints.api.models.http import Response
from application.use_cases import get_labels, get_receipt_list, add_receipt
from entrypoints.api.utils import json_resp
from .base import BaseHandler

logger = logging.getLogger(__name__)


@dataclass
class BudgetID(DataClassDictMixin):
    budget_id: str


class ListLabelsHandler(BaseHandler[BudgetID, None, None]):
    def __init__(self, db_sess: sessionmaker[AsyncSession]) -> None:
        self.session = db_sess
        super().__init__()

    async def handle(self, path_vars: BudgetID, query: None, body: None) -> Response:
        uc = get_labels.UseCase(UoW(self.session))
        res = await uc.execute(budget_id=path_vars.budget_id)
        return json_resp(Response(result=res))


@dataclass
class ReceiptUri(DataClassDictMixin):
    budget_id: str
    id: int


class GetReceiptHandler(BaseHandler[ReceiptUri, None, None]):
    def __init__(self, db_sess: sessionmaker[AsyncSession]) -> None:
        self.session = db_sess
        super().__init__()

    async def handle(self, path_vars: ReceiptUri, query: None, body: None) -> Response:
        # todo: make UC
        async with UoW(self.session) as uow:
            ret = await uow.receipts.get(id=path_vars.id, budget_id=path_vars.budget_id)
            await uow.commit()
        if ret:
            resp = ReceiptStruct.from_entity(ret)
            return json_resp(resp)
        raise HTTPNotFound()


@dataclass
class ListReceiptsFilter(DataClassDictMixin):
    labels: str | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class ListReceiptsHandler(BaseHandler[BudgetID, ListReceiptsFilter, None]):
    def __init__(self, db_sess: sessionmaker[AsyncSession]) -> None:
        self.session = db_sess
        super().__init__()

    async def handle(
            self,
            path_vars: BudgetID,
            query: ListReceiptsFilter,
            body: None
    ) -> Response:
        labels = query.labels.split(',') if query.labels else query.labels
        uc = get_receipt_list.UseCase(UoW(self.session))
        res = await uc.execute(
            budget_id=path_vars.budget_id,
            labels=labels,
            date_from=query.date_from,
            date_to=query.date_to
        )
        return json_resp(Response(result=[ReceiptStruct.from_entity(e) for e in res]))


class CreateReceiptHandler(BaseHandler[BudgetID, None, ReceiptCreateStruct]):
    def __init__(self, db_sess: sessionmaker[AsyncSession]) -> None:
        self.session = db_sess
        super().__init__()

    async def handle(
            self,
            path_vars: BudgetID,
            query: None,
            body: ReceiptCreateStruct
    ) -> Response:
        receipt = body.to_entity(path_vars.budget_id)
        uc = add_receipt.UseCase(UoW(self.session))
        new_receipt = await uc.execute(receipt)
        return json_resp(Response(result=ReceiptStruct.from_entity(new_receipt)))

