from uuid import uuid4
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.unit_of_work import UoW
from entrypoints.api.models.receipt import ReceiptStruct, ReceiptCreateStruct
from entrypoints.api.models.http import Response
from entrypoints.api.utils import json_resp

from application.use_cases import add_receipt
from .base import BaseHandler


class CreateBudgetHandler(BaseHandler[None, None, ReceiptCreateStruct]):
    def __init__(self, db_sess: sessionmaker[AsyncSession]) -> None:
        self.session = db_sess
        super().__init__()

    async def handle(
            self,
            path_vars: None,
            query: None,
            body: ReceiptCreateStruct
    ) -> Response:
        budget_id = uuid4().hex
        receipt = body.to_entity(budget_id)
        uc = add_receipt.UseCase(UoW(self.session))
        new_receipt = await uc.execute(receipt)
        return json_resp(Response(result=ReceiptStruct.from_entity(new_receipt)))

