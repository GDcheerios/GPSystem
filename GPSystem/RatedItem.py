from GPSystem.ItemType import ItemType
from GPSystem.Rating import Rating


class RatedItem:
    identifier: int
    rating: float
    name: str
    data: dict
    item_type: ItemType

    def __init__(self, id: int, name: str, data: dict, item_type: ItemType):
