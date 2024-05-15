from GPSystem.GPRater import GPRater
from GPSystem.ItemType import ItemType


class Ranking:
    rank: str
    tier: str

    def __init__(self, gp: int, item_type: ItemType = None):
        self.find_ranking(gp, item_type)

    def find_ranking(self, gp: int, item_type: ItemType):
        for tier_name, tier_values in reversed(GPRater.get_tiers(item_type).items()):
            for tier_value, gp_value in reversed(tier_values.items()):
                if gp >= gp_value:
                    if tier_name == "gentry warrior":
                        print(gp, tier_value)
                        print(int((gp / int(tier_value))))
                        self.rank = tier_name, self.tier = self.int_to_roman(int((gp / int(gp_value)) + 1))
                    else:
                        self.rank = tier_name, self.tier = self.int_to_roman(int(tier_value))
                    break

            if self.rank != 'unranked':
                break

    @staticmethod
    def int_to_roman(num: int) -> str:
        roman_numerals = {1000: 'M', 500: 'D', 100: 'C', 50: 'L', 10: 'X', 5: 'V', 4: 'IV', 1: 'I'}

        roman_str = ""
        for value, numeral in roman_numerals.items():
            while num >= value:
                roman_str += numeral
                num -= value

        return roman_str
