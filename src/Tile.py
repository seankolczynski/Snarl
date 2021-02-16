class Tile:

    def __init__(self, pos):
        self.position = pos
        self.object = None
        self.room = None

    def setObject(self, obj):
        self.object = obj

    def setRoom(self, room):
        self.room = room

    def draw(self):
        return " "


class WallTile:

    def __init__(self, pos):
        self.position = pos

    def draw(self):
        return "X"
