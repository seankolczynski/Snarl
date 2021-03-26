from Item import Item
from Adversary import Adversary
from Player import Player

class Tile(object):

    def __init__(self, pos):
        self.position = pos
        self.items = []
        self.room = None
        self.character = None

    def add_item(self, obj):
        self.items.append(Item(obj))
        return self

    def remove_item(self, obj):
        new_items = list(filter(lambda x: x.get_name != obj, self.items))
        self.items = new_items
    
    def get_character(self):
        return self.character

    def remove_character(self):
        self.character = None

    def set_room(self, room):
        self.room = room

    def get_room(self):
        return self.room 

    def get_item_with_name(self, name):
        for item in self.items:
            if item.get_name() == name:
                return item
        return None

    def get_all_items(self):
        return self.items

    def draw(self):
        if isinstance(self.character, Player):
            return "P"
        if isinstance(self.character, Adversary):
            return "A"
        for item in self.items:
            if item.get_name() == "Exit":
                return "e"
            if item.get_name() == "Potion":
                return "p"
            if item.get_name() == "Key" or item.get_name() == "key":
                return "k"
        return " "

    def add_character(self, character):
        response = {"success": True, "message": "OK"}
        if self.character != None:
            raise ValueError("Occupied!")
        self.character = character
        if isinstance(character, Player):
            for item in self.items:
                if item.name == "key" or item.name == "Key":
                    response = {"success": True, "message": "Key"}
                character.add_to_inventory(item)
            new_items = []
            self.items = new_items
            return response

    def get_position(self):
        return self.position

    def transfer_info(self, other):
        other.set_room(self.room)
        for item in self.items:
            other.add_item(item.get_name())
        return other

    def num_val(self):
        if self.room.door_at(self.position):
            return 2
        return 1

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.position == other.get_position()
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.position)

class WallTile(Tile):

    def __init__(self, pos):
        super().__init__(pos)

    def draw(self):
        return "X"

    def num_val(self):
        return 0


    def add_item(self, obj):
        raise TypeError("WallTile cannot have items")

    def add_character(self, character):
        raise TypeError("WallTile cannot have characters")

    def remove_character(self):
        raise TypeError("WallTile cannot have characters")

class ExitTile(Tile):

    def __init__(self, pos):
        super().__init__(pos)

    def draw(self):
        return "e"

