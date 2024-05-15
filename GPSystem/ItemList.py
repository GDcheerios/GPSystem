from GPSystem.Item import Item
from GPSystem.ItemType import ItemType


class ItemList(list):
    def __init__(self):
        super().__init__()

    def append(self, __object):
        super().append(__object)

        def sort_by_id(item: Item):
            return item.id

        self.sort(key=sort_by_id)

    def add_item(self, data: dict) -> None:
        self.append(Item(self.get_id(), data))

    def overwrite_item(self, id: int, data: dict) -> None:
        item_lookup = self.get_by_id(id)

        if item_lookup:
            self[self.index(item_lookup)] = Item(id, data)
        else:
            self.add_item(data)

    def get_by_id(self, id: int) -> Item:
        for item in self:
            if item.id == id:
                return item

    def get_id(self) -> int:
        current_id = 0

        for item in self:
            if (current_id + 1) == item.id:
                current_id += 1
            else:
                return current_id
