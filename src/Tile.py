class Tile(object):

    def __init__(self, pos):
        self.position = pos
        self.objects = []
        self.room = None
        self.character = None

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def setRoom(self, room):
        self.room = room

    def draw(self):
        if "Exit" in self.objects:
            return "e"
        return " "

    def add_character(self, character):
        if self.character != None:
            raise ValueError("Occupied!")
        self.character = character

    def remove_character(self):
        self.character = None

    def get_position(self):
        return self.position

class WallTile(Tile):

    def __init__(self, pos):
        self.position = pos

    def draw(self):
        return "X"
