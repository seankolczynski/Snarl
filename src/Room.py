
class Room:
    width = 0
    height = 0

    def __init__(self, tiles, position):
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.layout = tiles
        self.upperLeft = position
        self.doors = []

    def addDoor(self, door):
        self.doors.append(door)

