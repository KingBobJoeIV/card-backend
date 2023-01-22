from app.internal.helpers import get_origin
from app.internal.helpers.json_response import json_response
from flask import request


def not_found(e):
    return json_response(
        {"error": "not found"},
        status=404,
        headers={"access-control-allow-origin": get_origin(request)},
    )


def method_not_allowed(e):
    return json_response(
        {"error": "Method not allowed"},
        status=405,
        headers={"access-control-allow-origin": get_origin(request)},
    )
