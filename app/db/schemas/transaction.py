from ..base import db
from secrets import token_urlsafe


class Transaction(db.Model):
    tx_id: str = db.Column(db.TEXT, unique=True, nullable=False, primary_key=True)
    user_id: str = db.Column(db.TEXT, nullable=False)
    card_id: str = db.Column(db.TEXT, nullable=False)
    date: str = db.Column(db.JSON, nullable=False)
    amount: str = db.Column(db.TEXT, nullable=False)
    category: str = db.Column(db.TEXT, nullable=False)
    name: str = db.Column(db.TEXT, nullable=False)
    cards_used: str = db.Column(db.JSON, nullable=False)

    def __init__(
        self,
        card_id: str = None,
        user_id: str = None,
        date: str = None,
        amount: str = None,
        category: str = None,
        name: str = None,
        cards_used: str = None,
    ):
        self.card_id = card_id
        self.tx_id = token_urlsafe(20)
        self.user_id = user_id
        self.date = date
        self.amount = amount
        self.category = category
        self.name = name
        self.cards_used = cards_used

    @property
    def as_json(self):
        return {
            "card_id": self.card_id,
            "tx_id": self.id_,
            "user_id": self.user_id,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "name": self.name,
            "cards_used": self.cards_used,
        }
