from Item import Item
from Adversary import Adversary
from Player import Player

class Tile(object):

    def __init__(self, pos):
        self.position = pos
        self.items = []
        self.room = None
        self.character = None

    def add_object(self, obj):
        self.items.append(Item(obj))

    def remove_object(self, obj):
        new_items = filter(lambda x: x.name != obj, self.items)
        self.items = new_items

    def remove_character(self):
        self.character = None

    def setRoom(self, room):
        self.room = room

     def getRoom(self, room):
        return self.room 

    def get_item_with_name(self, name):
        for item in self.items():
            if item.get_name() == name:
                return item
        return None

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
        return " "

    def add_character(self, character):
        if self.character != None:
            raise ValueError("Occupied!")
        self.character = character
        for item in self.items:
            if item.name != "Exit":
                character.add_to_inventory(item)
        new_items = filter(lambda x: x.name == "Exit", self.items)
        self.items = new_items

    def get_position(self):
        return self.position

class WallTile(Tile):

    def __init__(self, pos):
        self.position = pos

    def draw(self):
        return "X"
