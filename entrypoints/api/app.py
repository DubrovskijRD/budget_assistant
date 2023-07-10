import logging
from functools import partial
from aiohttp import web
import aiohttp_cors


from infra.db.db import Db
from infra.db.models.base import Base
from config import settings
from entrypoints.api.handlers import receipt as receipt_api
from entrypoints.api.handlers import budget as budget_api
from infra.db.models.budget import BudgetEventModel

logging.basicConfig(level=logging.DEBUG)


def setup_router(app, db_sess):
    app.router.add_post('/b', budget_api.CreateBudgetHandler(db_sess))
    app.router.add_get('/b/{budget_id}/labels', receipt_api.ListLabelsHandler(db_sess))
    app.router.add_get(
        '/b/{budget_id}/receipts', receipt_api.ListReceiptsHandler(db_sess)
    )
    app.router.add_get(
        '/b/{budget_id}/receipts/{id}', receipt_api.GetReceiptHandler(db_sess)
    )
    app.router.add_post(
        '/b/{budget_id}/receipts', receipt_api.CreateReceiptHandler(db_sess)
    )


async def on_startup(db, app):
    # for middleware
    app['db_sess'] = db.session_factory
    async with db._engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    setup_router(app, db.session_factory)
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)


async def on_cleanup(db, app):
    await db.dispose()


@web.middleware
async def middleware(request: web.Request, handler):
    if budget_id := request.match_info.get('budget_id'):
        async with request.app['db_sess']() as sess:
            sess.add(BudgetEventModel(
                budget_id=budget_id,
                action=f'{request.method} {request.url}',
                user_ip=request.remote
            ))
            await sess.commit()
    resp = await handler(request)
    return resp


async def init():
    app = web.Application(middlewares=[middleware])
    db = Db(db_url=settings.DATABASE_URL)
    app.on_startup.append(partial(on_startup, db))
    app.on_cleanup.append(partial(on_cleanup, db))
    return app

if __name__ == '__main__':
    web.run_app(init())
