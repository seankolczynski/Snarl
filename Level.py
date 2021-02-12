class Level:

    def __init__(self, rooms, halls):
        rows, cols = (100, 100)
        self.grid = [[0 for i in range(cols)] for j in range(rows)]
        self.rooms = rooms
        self.halls = halls

    def draw(self):
        image = ""
        image += "┌"
        for x in range(98):
            image += "─"
        image += "┐\n"
        for y in range(98):
            image += "│"
            for x in range(98):
                image += " "
            image += "│\n"
        image += "└"
        for x in range(98):
            image += "─"
        image += "┘"
        print(image)


if __name__ == "__main__":
    level = Level([], [])
    level.draw()
