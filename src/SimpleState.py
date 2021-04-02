class SimpleState:
    def __init__(self, grid):
        self.grid = grid

    def render(self):
        return self.render_in_range((0, 0), -1)

    def render_in_range(self, position, FOV):
        upLeft = (0,0)
        downRight = (len(self.grid), len(self.grid[0]))
        layout = []
        observer = True
        if (FOV > 0):
            observer = False
            upLeft = ((position[0] - FOV), (position[1] - FOV))
            downRight = ((position[0] + FOV), (position[1] + FOV))
            for ind in range((FOV * 2) + 1):
                layout.append([])
        else:
            for inde in range(len(self.grid)):
                layout.append([])
        image = ""
        image += "+"
        for x in range(len(self.grid)):
            image += "--"
        image += "-+\n"
        for y in range(len(self.grid[0])):
            image += "| "
            count = 0
            for x in range(len(self.grid)):
                if observer or self.is_in_window(x, y, downRight, upLeft):
                    layout[count].append(self.grid[x][y])
                    count = count + 1
                    image += self.grid[x][y].draw()
                else:
                    image += " "
                image += " "
            image += "|\n"
        image += "+"
        for x in range(len(self.grid)):
            image += "--"
        image += "-+"
        print(image)
        return layout

    def is_in_window(self, x, y, downRight, upLeft):
        return (downRight[0] >= x >= upLeft[0]) and (downRight[1] >= y >= upLeft[1])

    def get_tile_at(self, pos):
        x, y = pos
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return self.grid[x][y]
        else:
            return None



