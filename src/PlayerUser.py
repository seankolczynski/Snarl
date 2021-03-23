
class PlayerUser:

    def __init__(self, type, ID, moves):
        self.move_sequence = moves
        self.ID = ID
        self.type = type
        self.gameState = None

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.type

    def request_move(self):
        return self.move_sequence.pop()

    def update_gamestate(self, gs, pos):
        self.gameState = gs
        self.render(pos)

    def render(self):
        image = ""
        image += "+"
        for x in range(3):
            image += "--"
        image += "-+\n"
        for y in range(3):
            image += "│ "
            for x in range(3):
                image += self.grid[x][y].draw()
                image += " "
            image += "│\n"
        image += "+"
        for x in range(3):
            image += "--"
        image += "-+"
        print(image)





    # This is a stub for testing
    def set_moves(self, moves):
        pass


# TODO Add Main Loop Logic