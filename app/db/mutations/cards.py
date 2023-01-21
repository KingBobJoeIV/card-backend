import json
from sqlalchemy.orm.attributes import flag_modified
from app.db.schemas import PhysicalCard
from app.db.schemas import VirtualCard
from app.db import db


def physical_card_info(provider, version, number, cvv, exp, name):
    return {
        "provider": provider,
        "version": version,
        "number": number,
        "cvv": cvv,
        "exp": exp,
        "name": name,
    }


def add_physicalcard_to_db(card_id, data, user_id):
    row = PhysicalCard(card_id, data, user_id)
    db.session.add(row)
    db.session.commit()


def add_virtualcard_to_db(card_id, number, cvv, expiry, address, zipcode):
    row = VirtualCard(card_id, number, cvv, expiry, address, zipcode)
    db.session.add(row)
    db.session.commit()


def remove_physicalcard(card_id):
    card = PhysicalCard.query.filter_by(card_id=card_id).first()
    setattr(card, "active", False)
    db.session.commit()


def remove_virtualcard(card_id):
    card = PhysicalCard.query.filter_by(card_id=card_id).first()
    setattr(card, "active", False)
    db.session.commit()


def choose_card_for_payment(category, amount, user_id):
    f = open("card_benefits.json")
    benefits = json.load(f)
    physical_cards = PhysicalCard.query.filter_by(id_=user_id).all()
    value = []
    for card in physical_cards:
        if category in benefits[card.name]:
            # the value/dollar we calculated at some point
            if benefits[card.name][card.blob["credit"]] >= amount:
                value.append((benefits[card.blob[card.name]][category], card.card_id))
    if value:
        return max(value)[1]
    return None


def charge_virtual_card(user_id, amount):
    card = VirtualCard.query.filter_by(user_id=user_id).first()
    setattr(card, "amount", card.amount - amount)
    db.session.commit()
