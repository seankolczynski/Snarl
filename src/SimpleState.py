class SimpleState:
    def __init__(self, grid):
        self.grid = grid
        self.layout = []


    def render(self):
        return self.render_in_range((0, 0), -1)

    def render_in_range(self, position, FOV):
        if position is None:
            return self.layout
        self.layout = []
        observer = True
        if (FOV > 0):
            observer = False
            self.upLeft = ((position[0] - FOV), (position[1] - FOV))
            self.upRight = ((position[0] + FOV), (position[1] - FOV))
            self.downLeft = ((position[0] - FOV), (position[1] + FOV))
            self.downRight = ((position[0] + FOV), (position[1] + FOV))
            for ind in range((FOV * 2) + 1):
                self.layout.append([])
        else:
            for inde in range(len(self.grid)):
                self.layout.append([])
        image = ""
        image += "+"
        for x in range(len(self.grid)):
            image += "--"
        image += "-+\n"
        for y in range(len(self.grid[0])):
            image += "│ "
            count = 0
            for x in range(len(self.grid)):
                if (observer or self.is_in_window(x, y)):
                    self.layout[count].append(self.grid[x][y])
                    count = count + 1
                    image += self.grid[x][y].draw()
                else:
                    image += " "
                image += " "
            image += "│\n"
        image += "+"
        for x in range(len(self.grid)):
            image += "--"
        image += "-+"
        #print(image)
        return self.layout

    def is_in_window(self, x, y):
        return (self.downRight[0] >= x >= self.upLeft[0]) and (self.downRight[1] >= y >= self.upLeft[1])


