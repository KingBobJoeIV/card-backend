from app.db.mutations.user import create_user
from app.db.mutations.cards import (
    add_physicalcard_to_db,
    remove_physicalcard,
    edit_physical_card,
    add_virtualcard_to_db,
    remove_virtualcard,
    list_transactions,
)
from app.db.mutations.util import commit
from app.db.queries.user import get_user_by_username

from app.decorators.api_response import api
from app.exceptions.app_exception import AppException
from app.internal.context import Context
from app.internal.helpers.json_response import json_response
from app.internal.security.auth_token import (
    authenticate,
    get_bearer_token,
    regenerate_access_token,
)
from app.db.queries.cards import get_physical_cards, get_virtual_cards
from app.internal.security.danger import create_token, decode_token
from app.models.user import (
    LoginModel,
    UserEditable,
    UserIn,
    UserOut,
    UserOutSecure,
)
from flask import Blueprint

from app.internal.helpers.random_card import card

router = Blueprint("user", __name__, url_prefix="/users")


@router.post("/-/register", strict_slashes=False)
@api.none
def register():
    req = Context()
    json = req.json
    pw = json.pop("password", None)
    print(req.json)
    body = UserIn(**req.json, password_hash=pw, is_admin=False)
    js = create_user(body, return_json=True)
    return {"user_data": js}


@router.post("/-/login")
@api.none
def login():
    req = Context(LoginModel)
    body = req.body
    access, refresh, user_data = authenticate(body.user, body.password)
    return json_response(
        {"user_data": user_data.as_json},
        headers={"x-access-token": access, "x-refresh-token": refresh},
    )


@router.get("/-/token/refresh")
@api.lax
def refresh_token():
    context = Context()
    headers = context.headers
    access_token = get_bearer_token(headers)
    decoded_access = decode_token(access_token)

    if decoded_access is None:
        refresh_token = headers.get("x-refresh-token")
        decoded_refresh = decode_token(refresh_token)
        access, refresh = regenerate_access_token(decoded_refresh)
        if access is None:
            raise AppException("re-auth")

        return json_response(
            {},
            headers={
                "x-access-token": create_token(access),
                "x-refresh-token": create_token(refresh),
            },
        )
    return {}


@router.get("/<user>/")
@api.strict
def user_details(user: str):
    req = Context()
    auth = req.auth
    is_me = user == "me"
    if is_me:
        if not auth.user:
            raise AppException("Not authenticated", 401)
        user = auth.user
    if user != auth.user:
        raise AppException("Not authorized")
    user_data = get_user_by_username(user)
    show_secure = user_data.user == auth.user or auth.is_admin
    model = (
        UserOutSecure.from_db(user_data) if show_secure else UserOut.from_db(user_data)
    )
    return {"user_data": model.dict()}


@router.patch("/<user>/")
@api.strict
def edit(user: str):
    req = Context()
    user = user.lower()
    if user != req.auth.user and not req.auth.is_admin:
        raise AppException("Not authorized to edit", 401)
    if not req.auth.is_admin:
        body = UserEditable(**req.json)
    else:
        body = UserIn(**req.json)
    user_data = get_user_by_username(user)
    user_data.user = body.user or user_data.user
    user_data.name = body.name or user_data.name
    json = user_data.as_json
    commit()
    return json


@router.get("/cards/physical/")
@api.strict
def api_get_physical_cards():
    req = Context()

    return {"cards": [x.as_json for x in get_physical_cards(req.auth.user_id)]}


@router.put("/cards/physical/")
@api.strict
def api_put_physical_cards():
    req = Context()
    json = req.json

    return add_physicalcard_to_db(json, req.auth.user_id)


@router.delete("/cards/physical/<card_id>")
@api.strict
def api_del_physical_cards(card_id):

    remove_physicalcard(card_id)
    return {}


@router.patch("/cards/physical/<card_id>")
@api.strict
def api_patch_physical_cards(card_id):
    req = Context()
    json = req.json
    return edit_physical_card(card_id, json)


@router.get("/cards/virtual")
@api.strict
def api_get_virtual_cards():
    req = Context()
    return {"cards": [x.as_json for x in get_virtual_cards(req.auth.user_id)]}


@router.post("/cards/virtual/create")
@api.strict
def api_create_virtual_card():
    import random

    req = Context()
    json = req.json
    c = card()
    return add_virtualcard_to_db(
        req.auth.user_id,
        req.auth.name,
        c,
        str(random.randint(1, 999)).zfill(3),
        {
            "month": str(random.randint(1, 12)).zfill(2),
            "year": str(random.randint(23, 30)).zfill(2),
        },
        "1 E Ohio St Indianapolis, IN",
        "46204",
        json,
    )


@router.delete("/cards/virtual/<card_id>")
@api.strict
def api_delete_virtual_card(card_id):
    print(card_id)
    remove_virtualcard(card_id)
    return {}


@router.get("/cards/transactions")
@api.strict
def api_get_tx():
    return [x.as_json for x in list_transactions(Context().auth.user_id)]
