"""Describes a layout of tiles. See examples in LevelTest.py"""
from Structures.Tile import WallTile, Tile

class Room:

    def __init__(self, tiles, position):
        self.upperLeft = position
        self.width = len(tiles)
        self.height = len(tiles[0])
        self.layout = self.generate_tiles(tiles)
        self.doors = {}

    def get_tile(self, pos):
        return self.layout[pos[0] - self.upperLeft[0]][pos[1] - self.upperLeft[1]]

    def get_origin(self):
        return self.upperLeft

    def room_width(self):
        return self.width

    def room_height(self):
        return self.height

    """
    Tile, Hallway
    Assigns the door to the hallway it leads to 
    """
    def addDoor(self, door, hall):
        self.doors[door] = hall

    def generate_tiles(self, tiles):
        grid = []
        x = len(tiles)
        y = len(tiles[0])
        offX = self.upperLeft[0]
        offY = self.upperLeft[1]
        for i in range(x):
            column = []
            for j in range(y):
                new_tile = None
                if tiles[i][j] == 0:
                    new_tile = WallTile((i + offX, j + offY))
                elif tiles[i][j] == 1:
                    new_tile = Tile((i + offX, j + offY))
                new_tile.set_room(self)
                column.append(new_tile)
            grid.append(column)
        return grid

    def return_neighbors(self):
        neighbors = []
        for door in self.doors:
            hall = self.doors[door]
            other = hall.otherside(self)
            neighbors.append(other)
        return neighbors

    """Checks if there is a door at this position."""
    def door_at(self, pos):
        for door in self.doors:
            if pos == door.get_position():
                return True
        return False





