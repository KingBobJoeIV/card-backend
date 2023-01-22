from app.db.schemas import PhysicalCard
from app.internal.helpers.guard import guard

message = "cards not found"


def get_physical_cards(user: str) -> list[PhysicalCard]:
    return PhysicalCard.query.filter_by(id_=user).all()
