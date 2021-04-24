
from PlayerUser import PlayerUser
import Common.JSONToLevel as JLevel
import json


class RemotePlayer(PlayerUser):

    def __init__(self, name, ctype, ID, server):
        super().__init__(name, ctype, ID)
        self.layout = None
        self.move_sequence = []
        self.ID = ID
        self.type = ctype
        self.gameState = None
        self.name = name
        self.server = server
        self.position = None
        self.message = ""

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def request_move(self):
        # print("your Position is: " + str(self.position))
        move_raw = self.server.read(self.ID)
        print("Stop")
        move = move_raw['to']
        print(move)
        try:
            if move is None:
                return self.position
            move_json = move
            formatted_move = (int(move_json[0]), int(move_json[1]))
            return formatted_move
        except:
            print("move failed")
            return self.request_move()


    def update_state(self, gs, pos):
        self.gameState = gs
        self.position = pos
        if pos is not None:
            exit = self.gameState.get_exit()
            exitPosn = ("exit", exit.get_position())
            output = {
            "type": "player-update",
            "layout": JLevel.player_layout(self.gameState.get_current_floor().grid, pos),
            "position": JLevel.translate_to_xy(pos),
            "objects": list(map(lambda x: {"type": x[0], "position": JLevel.translate_to_xy(x[1])}, (self.gameState.get_items() + [exitPosn]))),
            "actors": list(map(lambda x: {"type": x.ctype.value, "name": x.get_name(),
                                          "position": JLevel.translate_to_xy(x.get_char_position())},
                               list(filter(lambda y: y.is_alive() and not y.exited, self.gameState.get_players() + self.gameState.get_adversaries())))),
            "message": self.message
            }
            self.message = ""
            self.server.write_to_id(json.dumps(output), self.ID)

    def render(self, pos):
        pass

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
        self.message = message

# TODO Add Main Loop Logic
