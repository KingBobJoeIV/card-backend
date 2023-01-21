from ..base import db


class PhysicalCard(db.Model):
    card_id: str = db.Column(db.TEXT, unique=True, nullable=False, primary_key=True)
    blob: str = db.Column(db.JSON, nullable=False)
    id_: str = db.Column(db.TEXT, nullable=False)
    active: bool = db.Column(db.BOOLEAN, nullable=False)

    def __init__(
            self,
            card_id: str = None,
            blob: str = None,
            id_: str = None,
            active: bool = None):
        self.card_id = card_id
        self.blob = blob
        self.id_ = id_
        self.active = active

    @property
    def as_json(self):
        return {
            "card_id": self.card_id,
            "blob": self.blob,
            "id_": self.id_,
            "active": self.active,
        }
