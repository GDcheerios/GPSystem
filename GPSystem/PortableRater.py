from GPSystem.GPRater import GPRater
from GPSystem.GPmain import GPSystem
from GPSystem.ItemList import ItemList


class PortableRater:
    rater: GPRater
    characters: ItemList
    artifacts: ItemList
    weapons: ItemList

    def __init__(self, rater: GPRater):
        self.characters = ItemList()
        self.artifacts = ItemList()
        self.weapons = ItemList()

    def update_character(self, id: int, data: dict):
        self.characters.overwrite_item(id, data)

    def update_artifact(self, id: int, data: dict):
        self.artifacts.overwrite_item(id, data)

    def update_weapon(self, id: int, data: dict):
        self.weapons.overwrite_item(id, data)

    def add_character(self, data: dict):
        self.characters.add_item(data)

    def add_artifact(self, data: dict):
        self.artifacts.add_item(data)

    def add_weapon(self, data: dict):
        self.weapons.add_item(data)
