from GPSystem.ItemType import ItemType
from GPSystem.Ranking import Ranking


class Rating:
    weighted: float
    unweighted: float
    ranking: Ranking

    def __init__(self, weighted: float = 0, unweighted: float = 0, item_type: ItemType = None):
        self.weighted = weighted
        self.unweighted = unweighted
        self.ranking = Ranking(int(weighted) if not item_type else int(unweighted), item_type=item_type)
