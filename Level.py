import Room
import Hallway

class Level:

    def __init__(self, rooms, halls):
        self.rows, self.cols = (50, 50)
        self.grid = [["X" for i in range(self.cols)] for j in range(self.rows)]
        self.rooms = rooms
        self.halls = halls
        self.setupRooms()
        self.setupHallways(halls)


    def draw(self):
        image = ""
        image += "┌"
        for x in range(self.cols):
            image += "──"
        image += "┐\n"
        for y in range(self.rows):
            image += "│"
            for x in range(self.cols):
                image += self.grid[x][y]
                image += " "
            image += "│\n"
        image += "└"
        for x in range(self.cols):
            image += "──"
        image += "┘"
        print(image)

    def setupRooms(self):
        for room in self.rooms:
            offX, offY = room.upperLeft
            for x in range(room.width):
                for y in range(room.height):
                    tile = room.layout[x][y]
                    self.grid[x + offX][y + offY] = tile
                    test = self.grid[x + offX][y + offY]



    def setupHallways(self, halls):
        for h in halls:
            hallway = h.connectDots
            length = len(hallway)
            point = 0
            start = hallway[point]
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
                    while cursor <= big:
                        self.grid[cursor][startY] = "e"
                        cursor = cursor + 1
                if startX == nextX:
                    lil = min(startY, nextY)
                    big = max(startY, nextY)
                    cursor = lil
                    while cursor <= big:
                        self.grid[startX][cursor] = "e"
                        cursor = cursor + 1
                start = nextWay
            nextWay = hallway[len(hallway) - 1]
            startX = start[0]
            startY = start[1]
            nextX = nextWay[0]
            nextY = nextWay[1]
            if startY == nextY:
                lil = min(startX, nextX)
                big = max(startX, nextX)
                cursor = lil + 1
                while cursor < big - 1:
                    self.grid[cursor][startY] = "e"
                    cursor = cursor + 1
            if startX == nextX:
                lil = min(startY, nextY)
                big = max(startY, nextY)
                cursor = lil
                while cursor < big - 1:
                    self.grid[startX][cursor] = "e"
                    cursor = cursor + 1



    def validateTile(self, x, y):
        currentVal = self.grid[x][y]
        if currentVal == " ":
            raise ValueError("Given Invalid Layout. Please ensure your rooms and hallways do not overlap")





if __name__ == "__main__":
    example = [[" " for i in range(10)] for j in range(10)]
    hall = Hallway.Hallway((14, 5), (21, 5), [])
    zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
    room = Room.Room(example, [], (5, 5))
    room2 = Room.Room(example, [], (20, 5))
    level = Level([room, room2], [hall, zHall])
    level.draw()
