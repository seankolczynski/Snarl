"""Describes a layout of tiles. See examples in LevelTest.py"""
class Room:
    width = 0
    height = 0

    def __init__(self, tiles, position):
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.layout = tiles
        self.upperLeft = position
        self.doors = []

    def get_tile(self, pos):
        return self.layout[pos[0]][pos[1]]

    def get_origin(self):
        return self.upperLeft

    def addDoor(self, door):
        self.doors.append(door)




