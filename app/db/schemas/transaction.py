from ..base import db


class Transaction(db.Model):
    tx_id: str = db.Column(db.TEXT, unique=True, nullable=False, primary_key=True)
    card_id: str = db.Column(db.TEXT, nullable=False)
    date: str = db.Column(db.JSON, nullable=False)
    amount: str = db.Column(db.TEXT, nullable=False)
    category: str = db.Column(db.TEXT, nullable=False)
    name: str = db.Column(db.TEXT, nullable=False)

    def __init__(
        self,
        card_id: str = None,
        tx_id: str = None,
        date: str = None,
        amount: str = None,
        category: str = None,
        name: str = None,
    ):
        self.card_id = card_id
        self.tx_id = tx_id
        self.date = date
        self.amount = amount
        self.category = category
        self.name = name

    @property
    def as_json(self):
        return {
            "card_id": self.card_id,
            "tx_id": self.id_,
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "name": self.name,
        }
