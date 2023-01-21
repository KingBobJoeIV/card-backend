from ..base import db


class VirtualCard(db.Model):
    card_id: str = db.Column(db.TEXT, unique=True, nullable=False, primary_key=True)
    id_: str = db.Column(db.TEXT, nullable=False)
    card_number: str = db.Column(db.TEXT, nullable=False)
    card_cvv: str = db.Column(db.TEXT, nullable=False)
    card_expiry: str = db.Column(db.TEXT, nullable=False)
    card_address: str = db.Column(db.TEXT, nullable=False)
    card_zipcode: str = db.Column(db.TEXT, nullable=False)

    def __init__(
            self,
            card_id: str = None,
            id_: str = None,
            card_number: str = None,
            card_cvv: str = None,
            card_expiry: str = None,
            card_address: str = None,
            card_zipcode: str = None):
        self.card_id = card_id
        self.id_ = id_
        self.card_number = card_number
        self.card_cvv = card_cvv
        self.card_expiry = card_expiry
        self.card_address = card_address
        self.card_zipcode = card_zipcode

    @property
    def as_json(self):
        return {
            "card_id": self.card_id,
            "id_": self.id_,
            "card_number": self.card_number,
            "card_cvv": self.card_cvv,
            "card_expiry": self.card_expiry,
            "card_address": self.card_address,
            "card_zipcode": self.card_zipcode,
        }
