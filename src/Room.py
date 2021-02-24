"""Describes a layout of tiles. See examples in LevelTest.py"""
from Tile import WallTile, Tile

class Room:
    width = 0
    height = 0

    def __init__(self, tiles, position):
        self.upperLeft = position
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.layout = self.generate_tiles(tiles)
        self.doors = []

    def get_tile(self, pos):
        one = pos[0]
        two = pos[1]
        thre = self.upperLeft[0]
        four = self.upperLeft[1]
        lay = self.layout
        return self.layout[pos[0] - self.upperLeft[0]][pos[1] - self.upperLeft[1]]

    def get_origin(self):
        return self.upperLeft

    def addDoor(self, door):
        self.doors.append(door)

    def generate_tiles(self, tiles):
        grid = []
        x = len(tiles)
        y = len(tiles[0])
        offX = self.upperLeft[0]
        offY = self.upperLeft[1]
        for i in range(x):
            column = []
            for j in range(y):
                if tiles[i][j] == 0:
                    column.append(WallTile((i + offX, j + offY)))
                elif tiles[i][j] == 1:
                    column.append(Tile((i + offX, j + offY)))
            grid.append(column)
        return grid






