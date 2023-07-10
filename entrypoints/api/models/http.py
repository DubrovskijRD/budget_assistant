from msgspec import Struct


class Response(Struct):
    result: Struct
