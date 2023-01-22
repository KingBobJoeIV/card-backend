import json
import heapq
from sqlalchemy.orm.attributes import flag_modified
import datetime

from app.db import db
from app.db.schemas import PhysicalCard, VirtualCard, Transaction


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
    db.session.add(row)
    db.session.commit()
    return res


def add_virtualcard_to_db(id_, number, cvv, expiry, address, zipcode, config):
    row = VirtualCard(
        id_, number, cvv, expiry, address, zipcode, config=config, active=True
    )
    js = row.as_json
    db.session.add(row)
    db.session.commit()
    return js


def remove_physicalcard(card_id):
    card = PhysicalCard.query.filter_by(card_id=card_id).first()
    card.active = False
    db.session.commit()


def edit_physical_card(card_id: str, blob):
    card: PhysicalCard = PhysicalCard.query.filter_by(card_id=card_id).first()
    card.blob = {**card.blob, **blob}
    flag_modified(card, "blob")
    db.session.commit()
    return card.as_json


def remove_virtualcard(card_id):
    card = PhysicalCard.query.filter_by(card_id=card_id).first()
    card.active = False
    db.session.commit()


def choose_card_for_payment(company, category, amount, user_id, virtual_card_id):
    original_amount = amount
    f = open("card_benefits.json")
    benefits = json.load(f)
    f.close()
    virtual_card = VirtualCard.query.filter_by(
        id_=user_id, card_id=virtual_card_id
    ).first()
    credit = 0
    cards = heapq()
    if virtual_card.active:
        physical_card_ids = virtual_card.config["physical_ids"]
        if physical_card_ids:
            for id in physical_card_ids:
                physical_card = PhysicalCard.query.filter_by(
                    id_=user_id, card_id=id
                ).first()
                if physical_card.active:
                    blob = physical_card.blob
                    if (
                        blob["expiry"]["month"] >= datetime.now().month
                        and blob["expiry"]["year"] >= datetime.now().year
                    ):
                        credit += blob["limit"] - blob["spent"]
                        heapq.heappush(
                            cards,
                            (
                                -benefits[blob["provider"][blob["version"]][category]],
                                physical_card,
                            ),
                        )
                    else:
                        print(physical_card.card_id, "is expired!")
        else:
            print("there are no physical cards associated with the virtual card!")
    else:
        print("virtual card does not exist!")
    if credit < amount:
        print("you don't have enough funds!")
        return
    used = []
    while amount > 0:
        card = heapq.heappop(cards)
        temp = amount - (card.blob["limit"] - card.blob["spent"])
        if temp >= 0:
            amount -= card.blob["limit"] - card.blob["spent"]
            used.append((card.card_id, (card.blob["limit"] - card.blob["spent"])))
            card.blob["spent"] = card.blob["limit"]
        else:
            card.blob["spent"] += amount
            used.append((card.card_id, amount))
            amount = 0
        flag_modified(card, "blob")
    row = Transaction(
        card_id=virtual_card_id,
        date=datetime.datetime.now(),
        amount=original_amount,
        category=category,
        name=company,
        cards_used=used,
    )
    db.session.commit()
    print("purchase successful :D!")


def list_transactions(user_id):
    return Transaction.query.filter_by(user_id=user_id).all()
