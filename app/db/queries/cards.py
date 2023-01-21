from app.db.schemas import PhysicalCard
from app.internal.helpers.guard import guard

message = "cards not found"


def get_physical_cards(user: str) -> list[PhysicalCard]:
    return guard(PhysicalCard.filter_by(id_=user).all())
