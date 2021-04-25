
import random as r
from Structures.Tile import Tile, WallTile, ExitTile
from Structures.Room import Room
from Structures.Hallway import Hallway

"""
A floor is a data representation of the current floor being played on by the users. It maintains the entire layout of 
the game, including rooms and hallways, as well as where objects are. See examples in floorTest.py
"""


class Floor:

    def __init__(self, rooms, halls):
        self.rows, self.cols = (50, 50)
        self.grid = self.minGridSize(rooms, halls)
        self.rooms = rooms
        self.halls = halls
        self.setupRooms()
        self.setupHallways(halls)
        self.exit = None #self.makeExit()
        self.itemTiles = []

    def get_row_and_cols(self):
        return (self.rows, self.cols)

    def minGridSize(self, rooms, halls):
        maxX = 0
        maxY = 0
        for room in rooms:
            offX, offY = room.upperLeft
            width = room.room_width()
            height = room.room_height()
            maxX = max(maxX, offX + width)
            maxY = max(maxY, offY + height)
        for hall in halls:
            points = hall.get_waypoints()
            for point in points:
                maxX = max(maxX, point[0])
                maxY = max(maxY, point[1])
        maxX = maxX + 1
        maxY = maxY + 1
        self.cols = maxX
        self.rows = maxY
        return [[WallTile((i, j)) for j in range(maxY)] for i in range(maxX)]


    """Creates a low-res visual of the current game layout"""

    def draw(self):
        image = ""
        image += "+"
        for x in range(self.cols):
            image += "--"
        image += "-+\n"
        for y in range(self.rows):
            image += "| "
            for x in range(self.cols):
                image += self.grid[x][y].draw()
                image += " "
            image += "|\n"
        image += "+"
        for x in range(self.cols):
            image += "--"
        image += "-+"
        print(image)
        return image

    """Places the rooms in the floor and ensures they are valid"""

    def setupRooms(self):
        for roomie in self.rooms:
            offX, offY = roomie.upperLeft
            for x in range(roomie.width):
                for y in range(roomie.height):
                    self.validateTile(x + offX, y + offY)
                    spot = roomie.get_tile((x + offX, y + offY))
                    self.grid[x + offX][y + offY] = spot

    """Places Hallways in the floor and confirms validity"""

    def setupHallways(self, halls):
        for h in halls:
            start, end, tiles = h.generate_tiles()
            door1 = self.grid[start[0]][start[1]]
            room1 = door1.get_room()
            room1.addDoor(door1, h)
            h.add_start(door1)
            door2 = self.grid[end[0]][end[1]]
            room2 = door2.get_room()
            room2.addDoor(door2, h)
            h.add_end(door2)
            for t in tiles:
                x, y = t.get_position()
                self.validateTile(x, y)
                self.grid[x][y] = t


    """Ensures that no Tile is placed where another exists. If one is, it throws an error, as the layout is invalid."""

    def validateTile(self, x, y):
        currentVal = self.grid[x][y]
        if type(currentVal) is not WallTile:
            raise ValueError("Given Invalid Layout. Please ensure your rooms and hallways do not overlap")

    """Randomly places the exit in a room of the floor"""

    def makeExit(self):
        roomRange = len(self.rooms)
        roomChoiceNum = r.randint(0, roomRange - 1)
        roomChoice = self.rooms[roomChoiceNum]
        coordX = r.randint(0, roomChoice.width - 1)
        coordY = r.randint(0, roomChoice.height - 1)
        offX, offY = roomChoice.upperLeft

        if type(self.grid[offX + coordX][offY + coordY]) == Tile:
            self.grid[offX + coordX][offY + coordY] = ExitTile((offX + coordX,offY + coordY))
            return self.grid[offX + coordX][offY + coordY]
        else:
            self.makeExit()

    def get_tile_at(self, pos):
        x, y = pos
        if x < self.cols and y < self.rows:
            return self.grid[x][y]
        else:
            raise ValueError("Out of Level Bounds. Please move somewhere within")

    def set_exit(self, pos):
        new_exit = ExitTile(pos)
        if self.exit is not None:
            old_exit_x, old_exit_y = self.exit.get_position()
            self.grid[old_exit_x][old_exit_y] = Tile((old_exit_x, old_exit_y))
            new_exit = self.exit.transfer_info(new_exit)
        oldTile = self.grid[pos[0]][pos[1]]
        self.grid[pos[0]][pos[1]] = new_exit
        new_exit = oldTile.transfer_info(new_exit)
        self.exit = new_exit


    def get_exit(self):
        return self.exit

    def place_item(self, item, pos):
        receiving = self.grid[pos[0]][pos[1]]
        if not isinstance(receiving, WallTile):
            receiving.add_item(item)
            self.grid[pos[0]][pos[1]] = receiving
            self.itemTiles.append(receiving)
            return receiving

    def get_room_from_pos(self, pos):
       raw_tile = self.grid[pos[0]][pos[1]] 
       return raw_tile.get_room()

    def reaches(self, structure):
        return structure.return_neighbors()

    def get_items(self):
        itemPosns = []
        for tile in self.itemTiles:
            pos = tile.get_position()
            items = tile.get_all_items()
            for item in items:
                itemPosns.append((item.get_name(), pos))
        return itemPosns

    def check_if_unlocked(self):
        itemPosns = self.get_items()
        for item in itemPosns:
            if item[0] == "key" or item[1] == "Key":
                return False
        return True



if __name__ == "__main__":
    example = [[Tile((i, j)) for i in range(10)] for j in range(10)]
    hall = Hallway((14, 5), (21, 5), [])
    zHall = Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
    room = Room(example, (5, 5))
    room2 = Room(example, (20, 5))
    floor = Floor([room, room2], [hall, zHall])
    floor.draw()
