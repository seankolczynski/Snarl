class Tile(object):

    def __init__(self, pos):
        self.position = pos
        self.items = []
        self.room = None
        self.character = None

    def add_object(self, obj):
        self.items.append(obj)

    def remove_object(self, obj):
        self.items.remove(obj)

    def remove_character(self):
        self.character = None

    def setRoom(self, room):
        self.room = room

    def draw(self):
        if "Exit" in self.items:
            return "e"
        return " "

    def add_character(self, character):
        if self.character != None:
            raise ValueError("Occupied!")
        self.character = character
        for item in self.items:
            if item.name is not "Exit":
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
