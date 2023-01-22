from flask import Blueprint
from app.internal.helpers import send_static_file
from app.decorators.api_response import api
from app.internal.context import Context
from app.db.mutations.cards import choose_card_for_payment, find_virtualcard
from app.internal.helpers.guard import guard

router = Blueprint("common", __name__)


@router.get("/favicon.ico")
def favicon():
    return send_static_file("favicon.ico")


@router.get("/robots.txt")
def robots():
    return send_static_file("robots.txt")


@router.post("/api/transaction-handler")
@api.none
def tx_handler():
    """
    Note about this function:
    Outside of the sandbox of this hackathon, we would be responding to a
    stripe_payment intent webhook. But since we cannot have virtual cards generated
    for testing (this costs real money and in development it could well be
    hundreds of dollars)
    so we have our own payment handler interface and isntead of this being a webhook,
    this IS a stripe replacement
    in an actual production environemtn
    """
    ctx = Context()
    json = ctx.json

    vc = find_virtualcard(
        guard(json.get("name"), "Name needed"),
        guard(json["cardnumber"], "Card number needed"),
    )
    return choose_card_for_payment(
        guard(json.get("company"), "Company needed"),
        guard(json.get("category"), "purchase category needed"),
        float(guard(json.get("amount") or "0", "amount needed")),
        vc.id_,
        vc,
    )
