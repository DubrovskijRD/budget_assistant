from aiohttp.web import json_response, Response
from msgspec import json


def json_resp(model) -> Response:
    body = json.encode(model)
    return json_response(body=body)
