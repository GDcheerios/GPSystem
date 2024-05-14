from GPSystem.Ranking import Ranking


class Rating:
    unweighted: float
    weighted: float
    ranking: Ranking

    def __init__(self, weighted: float = 0, unweighted: float = 0):
        self.weighted = weighted
        self.unweighted = unweighted
        self.ranking = Ranking(int(weighted))

    def get_rounded(self, digits: int = 0):
        weighted = round(self.weighted, digits)
        unweighted = round(self.unweighted, digits)
        return Rating(weighted, unweighted)
