
class PlayerUser:

    def __init__(self, type, ID):
        self.ID = ID
        self.type = type
        self.gameState = None

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.type

    def request_move(self):
        return self.move_sequence.pop()

    def update_gamestate(self, gs):
        self.gameState = gs

    # This is a stub for testing
    def set_moves(self, moves):
        self.move_sequence = moves


# TODO Add Main Loop Logic