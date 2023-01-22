from app.db.schemas import PhysicalCard, VirtualCard


message = "cards not found"


def get_physical_cards(user: str) -> list[PhysicalCard]:
    return PhysicalCard.query.filter_by(id_=user).all()


def get_virtual_cards(user: str) -> list[VirtualCard]:
    return VirtualCard.query.filter_by(id_=user).all()
