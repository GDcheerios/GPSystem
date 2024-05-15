from GPSystem.Rating import Rating


class Item:
    id: int
    data: dict
    rating: Rating

    def __init__(self, id: int, data: dict):
        self.id = id
        self.data = data

        self.rating = rating
