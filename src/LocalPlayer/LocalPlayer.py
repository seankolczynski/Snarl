
from PlayerUser import PlayerUser
import json


class LocalPlayer(PlayerUser):

    def __init__(self, name, ctype, ID):
        super().__init__(name, ctype, ID)
        self.layout = None
        self.move_sequence = []
        self.ID = ID
        self.type = ctype
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
        # print("your Position is: " + str(self.position))
        move_raw = input("give move")
        move = move_raw["to"]
        try: 
            if move == None:
                return self.position
            move_json = move
            if not (isinstance(move_json[0], int)):
                raise ValueError("the first value is not a number")
            if not (isinstance(move_json[1], int)):
                raise ValueError("the second value is not a number")
            formatted_move = (move_json[0], move_json[1])
            return formatted_move
        except:
            return self.request_move()


    def update_state(self, gs, pos):
        self.gameState = gs
        self.position = pos
        if pos is not None:
            self.render(pos)

    def render(self, pos):
        print(self.name + "'s View:")
        return self.gameState.render_in_range(pos, 2)

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

    # This is a stub for testing
    def set_moves(self, moves):
        pass

    def transmit_message(self, message):
        print(message)

# TODO Add Main Loop Logic
