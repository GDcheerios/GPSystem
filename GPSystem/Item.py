from GPSystem.GPRater import GPRater
from GPSystem.ItemType import ItemType
from GPSystem.Rating import Rating


class Item:
    id: int
    data: dict
    rating: Rating
    item_type: ItemType

    def __init__(self, id: int, data: dict):
        self.id = id
        self.data = data
        self.rating = Rating(unweighted=GPRater.get_rater_by_type(self)(self.data), item_type=GPRater.get_item_type(self.data))
