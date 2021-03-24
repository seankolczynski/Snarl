class SimpleState:
    def __init__(self, grid):
        self.grid = grid


    def render(self):
        return self.render_in_range((0, 0), -1)

    def render_in_range(self, position, range):
        observer = True
        if (range > 0):
            observer = False
            self.upLeft = ((position[0] - range), (position[1] - range))
            self.upRight = ((position[0] + range), (position[1] - range))
            self.downLeft = ((position[0] - range), (position[1] + range))
            self.downRight = ((position[0] + range), (position[1] + range))

        image = ""
        image += "+"
        for x in range(len(self.grid)):
            image += "--"
        image += "-+\n"
        for y in range(len(self.grid[0])):
            image += "│ "
            for x in range(len(self.grid)):
                if (observer or self.is_in_window(x, y)):
                    image += self.grid[x][y].draw()
                else:
                    image += " "
                image += " "
            image += "│\n"
        image += "+"
        for x in range(len(self.grid)):
            image += "--"
        image += "-+"
        print(image)

    def is_in_window(self, x, y):
        return (self.downRight[0] >= x >= self.upLeft[0]) and (self.downRight[1] >= y >= self.upLeft[1])


