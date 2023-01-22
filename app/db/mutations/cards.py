import heapq
import json
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm.attributes import flag_modified

from app.db import db
from app.db.schemas import PhysicalCard, Transaction, VirtualCard
from app.exceptions.app_exception import AppException
from app.internal.helpers.guard import guard


def physical_card_info(provider, version, number, cvv, exp, name, limit):
    return {
        "provider": provider,
        "version": version,
        "number": number,
        "cvv": cvv,
        "exp": exp,
        "name": name,
        "limit": limit,
    }


def add_physicalcard_to_db(data, user_id):
    row = PhysicalCard(data, user_id)
    res = row.as_json
    # pylint:disable=no-member
    db.session.add(row)
    db.session.commit()
    return res


def add_virtualcard_to_db(id_, name, number, cvv, expiry, address, zipcode, config):
    # pylint:disable=no-member
    row = VirtualCard(
        id_=id_,
        name=name,
        card_address=address,
        card_expiry=expiry,
        card_cvv=cvv,
        card_number=number,
        card_zipcode=zipcode,
        config=config,
    )
    js = row.as_json
    db.session.add(row)
    db.session.commit()
    return js


def remove_physicalcard(card_id):
    # pylint:disable=no-member
    card = PhysicalCard.query.filter_by(card_id=card_id).first()
    card.active = False
    db.session.commit()


def edit_physical_card(card_id: str, blob):
    # pylint:disable=no-member
    card: PhysicalCard = PhysicalCard.query.filter_by(card_id=card_id).first()
    card.blob = {**card.blob, **blob}
    flag_modified(card, "blob")
    db.session.commit()
    return card.as_json


def remove_virtualcard(card_id):
    # pylint:disable=no-member
    card = VirtualCard.query.filter_by(card_id=card_id).first()
    card.active = False
    db.session.commit()


f = Path() / "app" / "core/card_benefits.json"
benefits = json.loads(f.read_text())


def find_virtualcard(name, card_number) -> VirtualCard:
    return VirtualCard.query.filter_by(name=name, card_number=card_number).first()


def choose_card_for_payment(
    company, category, amount, user_id, virtual_card: VirtualCard
):
    original_amount = amount
    virtual_card_id = virtual_card.card_id
    credit = 0
    cards = []
    if virtual_card.active:
        physical_card_ids = virtual_card.config["physical_ids"]
        if physical_card_ids:
            for id in physical_card_ids:
                physical_card: PhysicalCard = guard(
                    PhysicalCard.query.filter_by(id_=user_id, card_id=id).first(),
                    "Physical card not found",
                )
                if physical_card.active:
                    blob = physical_card.blob
                    if (
                        blob["expiry"]["month"] >= datetime.now().month
                        and blob["expiry"]["year"] >= datetime.now().year
                    ):
                        credit += blob["limit"] - blob["spent"]
                        try:
                            cat = benefits[blob["provider"]][blob["version"]][category]
                        except Exception as e:
                            print(e)
                            cat = 0
                        heapq.heappush(
                            cards,
                            (
                                -cat,
                                physical_card,
                            ),
                        )
                    else:
                        raise AppException(physical_card.card_id + " is expired!")
        else:
            raise AppException(
                "there are no physical cards associated with the virtual card!"
            )
    else:
        raise AppException("virtual card does not exist!")
    if credit < amount:
        raise AppException("you don't have enough funds!")
    used = []
    while amount > 0:
        card = heapq.heappop(cards)[1]
        card_blob = {**card.blob}
        temp = amount - (card_blob["limit"] - card_blob["spent"])
        if temp >= 0:
            amount -= card_blob["limit"] - card_blob["spent"]
            used.append((card.card_id, (card_blob["limit"] - card_blob["spent"])))
            card_blob["spent"] = card_blob["limit"]
        else:
            card_blob["spent"] += amount

            used.append((card.card_id, amount))
            amount = 0
        card.blob = card_blob
        flag_modified(card, "blob")
    cfg = {**virtual_card.config}
    cfg["spent"] += amount
    virtual_card.config = cfg
    flag_modified(virtual_card, "config")
    from time import time

    row = Transaction(
        card_id=virtual_card_id,
        date=f"{time()}",
        amount=original_amount,
        category=category,
        name=company,
        cards_used=used,
        user_id=user_id,
    )
    # pylint:disable=no-member
    db.session.add(row)
    db.session.commit()
    return row.as_json


def list_transactions(user_id) -> list[Transaction]:
    return Transaction.query.filter_by(user_id=user_id).all()
