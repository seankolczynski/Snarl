from Common.Observer import Observer


class PlayerUser(Observer):

    def __init__(self, name, type, ID):
        super().__init__(id)
        self.layout = None
        self.move_sequence = []
        self.ID = ID
        self.type = type
        self.gameState = None
        self.name = name
        self.position = None

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def request_move(self):
        if len(self.move_sequence) > 0:
            move = self.move_sequence.pop(0)
            #if move is None:
            #    return self.position
            return move
        else:
            raise ValueError("Out of moves")

    def update_state(self, gs, pos):
        self.gameState = gs
        self.position = pos
        if pos is not None:
            self.render(pos)

    def render(self, pos):
        self.gameState.render_in_range(pos, 2)

    """For Tests"""
    def get_next_move(self):
        if len(self.move_sequence) > 0:
            move = self.move_sequence[0]
            if move is None:
                return self.position
            return move
        return None

    def get_view(self):
        self.layout = self.gameState.render_in_range(self.position, 2)
        return self.layout

    def get_position(self):
        return self.position

    def transmit_message(self, message):
        pass


    # This is a stub for testing
    def set_moves(self, moves):
        pass
