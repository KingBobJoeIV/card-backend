from ..base import db
from secrets import token_urlsafe


class VirtualCard(db.Model):
    card_id: str = db.Column(db.TEXT, unique=True, nullable=False, primary_key=True)
    id_: str = db.Column(db.TEXT, nullable=False)
    name: str = db.Column(db.TEXT, nullable=False)
    card_number: str = db.Column(db.TEXT, nullable=False)
    card_cvv: str = db.Column(db.TEXT, nullable=False)
    card_expiry: dict = db.Column(db.JSON, nullable=False)
    card_address: str = db.Column(db.TEXT, nullable=False)
    card_zipcode: str = db.Column(db.TEXT, nullable=False)
    card_limit: str = db.Column(db.TEXT, nullable=False, default="@NA")
    active: bool = db.Column(db.BOOLEAN, nullable=False)
    config: dict = db.Column(db.JSON, default={})


    def __gt__(self,other):
        return 0
    

    def __init__(
        self,
        id_: str = None,
        name: str = None,
        card_number: str = None,
        card_cvv: str = None,
        card_expiry: str = None,
        card_address: str = None,
        card_zipcode: str = None,
        card_limit: str = None,
        config: dict = None,
        active: bool = True,
    ):
        self.card_id = token_urlsafe(20)
        self.id_ = id_
        self.name = name
        self.card_number = card_number
        self.card_cvv = card_cvv
        self.card_expiry = card_expiry
        self.card_address = card_address
        self.card_zipcode = card_zipcode
        self.card_limit = card_limit
        self.active = active
        self.config = config or {}
        self.config["spent"] = 0

    @property
    def as_json(self):
        return {
            "card_id": self.card_id,
            "id_": self.id_,
            "name": self.name,
            "card_number": self.card_number,
            "card_cvv": self.card_cvv,
            "card_expiry": self.card_expiry,
            "card_address": self.card_address,
            "card_zipcode": self.card_zipcode,
            "card_limit": self.card_limit,
            "active": self.active,
            "config": self.config,
        }
