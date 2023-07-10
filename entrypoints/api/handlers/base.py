from abc import ABC, abstractmethod
from typing import Generic, TypeVar, get_args
from types import NoneType
from aiohttp.web import Request, Response
from msgspec import Struct
from msgspec.json import Decoder
from mashumaro.mixins.dict import DataClassDictMixin

P = TypeVar('P', bound=DataClassDictMixin | None)
Q = TypeVar('Q', bound=DataClassDictMixin | None)
B = TypeVar('B', bound=Struct | None)


class BaseHandler(ABC, Generic[P, Q, B]):

    def __init__(self):
        path_type, query_type, body_type = get_args(
            self.__orig_bases__[0]  # type: ignore
        )
        self._path_type = path_type
        self._query_type = query_type
        self._body_type = body_type
        self._decoder: Decoder[B] | None = (Decoder(body_type)
                                            if body_type is not NoneType
                                            else None)

    async def __call__(self, request: Request) -> Response:
        path_vars = self._get_path_vars(request)
        query = self._get_query(request)
        body = await self._get_body(request)
        # todo: headers
        return await self.handle(path_vars=path_vars, query=query, body=body)

    @abstractmethod
    async def handle(self, path_vars: P, query: Q, body: B) -> Response:
        pass

    def _get_query(self, request: Request) -> Q:
        return (self._query_type.from_dict(request.query)
                if self._query_type is not NoneType
                else None)

    def _get_path_vars(self, request: Request) -> P:
        return (self._path_type.from_dict(request.match_info)
                if self._path_type is not NoneType
                else None)

    async def _get_body(self, request) -> B:
        if self._body_type is NoneType:
            return None
        data = await request.read()
        obj = self._decoder.decode(data)
        return obj
