import Hallway, Room
import random as r
from Tile import Tile, WallTile

"""
A floor is a data representation of the current floor being played on by the users. It maintains the entire layout of 
the game, including rooms and hallways, as well as where objects are. See examples in floorTest.py
"""
class Floor:

    def __init__(self, rooms, halls):
        self.rows, self.cols = (50, 50)
        self.grid = [[WallTile((i, j)) for i in range(self.cols)] for j in range(self.rows)]
        self.rooms = rooms
        self.halls = halls
        self.setupRooms()
        self.setupHallways(halls)
        self.exit = self.makeExit()

    """Increases the default size of the board if needed"""
    def expandGrid(self, new_height, new_width):
        for j in range(self.rows):
            self.grid[j] = self.grid[j] + [WallTile((i, j)) for i in range(new_width - self.cols)]
        for i in range(new_width - self.rows):
            self.grid.append([WallTile((i, j)) for j in range(new_height)])
        self.rows, self.cols = (new_height, new_width)

    """Creates a low-res visual of the current game layout"""
    def draw(self):
        image = ""
        image += "┌"
        for x in range(self.cols):
            image += "──"
        image += "─┐\n"
        for y in range(self.rows):
            image += "│ "
            for x in range(self.cols):
                image += self.grid[x][y].draw()
                image += " "
            image += "│\n"
        image += "└"
        for x in range(self.cols):
            image += "──"
        image += "─┘"
        print(image)

    """Places the rooms in the floor and ensures they are valid"""
    def setupRooms(self):
        for roomie in self.rooms:
            offX, offY = roomie.upperLeft
            if offX + roomie.width > self.cols or offY + roomie.height > self.rows:
                self.expandGrid(offX + roomie.width, offY + roomie.height)
            for x in range(roomie.width):
                for y in range(roomie.height):
                    self.validateTile(x + offX, y + offY)
                    spot = Tile((x + offX, y + offY))
                    spot.setRoom(roomie)
                    self.grid[x + offX][y + offY] = spot

    """Places Hallways in the floor and confirms validity"""
    def setupHallways(self, halls):
        for h in halls:
            hallway = h.connectDots
            length = len(hallway)
            point = 0
            start = hallway[point]
            door1 = self.grid[start[0]][start[1]]
            roomie = door1.room
            roomie.addDoor(start)
            for way in range(len(hallway) - 1):
                if way != 0:
                    self.validateTile(hallway[way][0], hallway[way][1])
                    self.grid[hallway[way][0]][hallway[way][1]] = Tile((hallway[way][0], hallway[way][1]))
            while point < length - 2:
                nextWay = hallway[point + 1]
                point = point + 1
                startX = start[0]
                startY = start[1]
                nextX = nextWay[0]
                nextY = nextWay[1]
                if startY == nextY:
                    lil = min(startX, nextX)
                    big = max(startX, nextX)
                    cursor = lil + 1
                    while cursor < big:
                        self.validateTile(cursor, startY)
                        self.grid[cursor][startY] = Tile((cursor, startY))
                        cursor = cursor + 1
                if startX == nextX:
                    lil = min(startY, nextY)
                    big = max(startY, nextY)
                    cursor = lil + 1
                    while cursor < big:
                        self.validateTile(startX, cursor)
                        self.grid[startX][cursor] = Tile((startX, cursor))
                        cursor = cursor + 1
                start = nextWay
            nextWay = hallway[len(hallway) - 1]
            door2 = self.grid[nextWay[0]][nextWay[1]]
            roomie = door2.room
            roomie.addDoor(nextWay)
            startX = start[0]
            startY = start[1]
            nextX = nextWay[0]
            nextY = nextWay[1]
            if startY == nextY:
                lil = min(startX, nextX)
                big = max(startX, nextX)
                cursor = lil + 1
                while cursor < big - 1:
                    self.validateTile(cursor, startY)
                    self.grid[cursor][startY] = Tile((cursor, startY))
                    cursor = cursor + 1
            if startX == nextX:
                lil = min(startY, nextY)
                big = max(startY, nextY)
                cursor = lil
                while cursor < big - 1:
                    self.validateTile(startX, cursor)
                    self.grid[startX][cursor] = Tile((startX, cursor))
                    cursor = cursor + 1

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
            self.grid[offX + coordX][offY + coordY].add_object("Exit")
            return self.grid[offX + coordX][offY + coordY]
        else:
            self.makeExit()

    def get_tile_at(self, pos):
        x, y = pos
        if x < self.cols and y < self.rows:
            return self.grid[x][y]
        # Else?

    def set_exit(self, pos):
        if self.exit is not None:
            self.exit.remove_object("Exit")
        self.exit = self.grid[pos[0]][pos[1]]
        self.exit.add_object("Exit")

    def get_exit(self):
        return self.exit

    def place_item(self, item, pos):
        receiving = self.grid[pos[0]][pos[1]]
        if not isinstance(receiving, WallTile):
            receiving.add_object(item)


if __name__ == "__main__":
    example = [[Tile((i, j)) for i in range(10)] for j in range(10)]
    hall = Hallway.Hallway((14, 5), (21, 5), [])
    zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
    room = Room.Room(example, (5, 5))
    room2 = Room.Room(example, (20, 5))
    floor = Floor([room, room2], [hall, zHall])
    floor.draw()

