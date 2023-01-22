from ..base import db
from secrets import token_urlsafe


class PhysicalCard(db.Model):
    card_id: str = db.Column(db.TEXT, unique=True, nullable=False, primary_key=True)
    blob: str = db.Column(db.JSON, nullable=False)
    id_: str = db.Column(db.TEXT, nullable=False)
    active: bool = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(
        self,
        blob: str = None,
        id_: str = None,
        active: bool = None,
    ):
        self.card_id = token_urlsafe(20)
        self.blob = blob or {}
        self.blob["limit"] = 500
        self.blob["spent"] = 0
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
