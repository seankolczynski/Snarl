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
            hallway =h.connectDots
            if hallway:
                length = len(hallway)
                start = hallway[0]
                point = 1
                while point < length:
                    next = hallway[point]
                    point = point + 1
                    startX = start[0]
                    startY = start[1]
                    nextX = next[0]
                    nextY = next[1]
                    if startX == nextX:
                        lil = min(startY, nextY)
                        big = max(startY, nextY)
                        cursor = lil
                        while cursor < big:
                            self.grid[cursor][startX] = " "
                            cursor = cursor + 1





if __name__ == "__main__":
    example = [[" " for i in range(10)] for j in range(10)]
    hall = Hallway.Hallway((5, 15), (5, 20), [])
    room = Room.Room(example, [], (5, 5))
    room2 = Room.Room(example, [], (20, 5))
    level = Level([room, room2], [hall])
    level.draw()
