from Enums.CharacterType import CharacterType
from Beings.Hero import Hero
from Beings.Zombie import Zombie
from Beings.Ghost import Ghost
from PlayerUser import PlayerUser
import Common.JSONToLevel as JLevel
import json


def manhattan_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)


def make_of_type(name, ctype, ID):
    if ctype == CharacterType.PLAYER:
        return Hero(2, ID, name)
    elif ctype == CharacterType.ZOMBIE:
        return Zombie(ID, name)
    elif ctype == CharacterType.GHOST:
        return Ghost(ID, name)


class RemoteAdversary(PlayerUser):

    def __init__(self, name, ctype, ID, server):
        super().__init__(name, ctype, ID)
        self.adversary = make_of_type(name, ctype, ID)
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
        return self.adversary.get_id()

    def get_type(self):
        return self.adversary.get_type()

    def get_name(self):
        return self.adversary.get_name()

    """Called by the GameManager, requests the first of the list of options"""

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

    """Called by GameManager, provides our position and the simple gamestate. If position changes (aka we have moved), we update our current surroundings"""

    def update_state(self, gs, pos):
        self.gameState = gs
        self.position = pos
        if pos is not None:
            exit = self.gameState.get_exit()
            exitPosn = ("exit", exit.get_position())
            output = {
                "type": "player-update",
                "layout": JLevel.adversary_view(self.gameState.get_current_floor().grid),
                "position": JLevel.translate_to_xy(pos),
                "objects": list(map(lambda x: {"type": x[0], "position": JLevel.translate_to_xy(x[1])},
                                    (self.gameState.get_items() + [exitPosn]))),
                "actors": list(map(lambda x: {"type": x.ctype.value, "name": x.name,
                                              "position": JLevel.translate_to_xy(x.get_char_position())},
                                   list(filter(lambda y: y.is_alive() and not y.exited,
                                               self.gameState.get_players() + self.gameState.get_adversaries())))),
                "message": self.message
            }
            self.message = ""
            self.server.write_to_id(json.dumps(output), self.ID)


    """For Tests"""

    def get_next_move(self):
        if len(self.move_sequence) > 0:
            move = self.move_sequence[0]
            if move is None:
                return self.position
            return move
        return None

    """Draws the """

    def render(self, pos):
        pass
        # self.layout = self.gameState.render()
        # return self.layout

    def get_position(self):
        return self.position

    """
    Returns a list of move options, in order of priority, based on the immediate area surrounding our position
    """
    def pick_moves(self):
        targets_in_radius = []
        radius = 1
        moves = []
        while radius <= self.vision:
            upLeft = (self.position[0] - radius, self.position[1] - radius)
            bottomRight = (self.position[0] + radius, self.position[1] + radius)
            targets_in_radius.extend(self.ring(upLeft, bottomRight))
            radius = radius + 1
        if len(targets_in_radius) > 0:
            sorted_targets = self.adversary.prioritize(targets_in_radius, self.gameState)
            for target in sorted_targets:
                chased = self.chase(target)
                for cha in chased:
                    if cha not in moves and self.adversary.fit_the_bill(self.gameState.get_tile_at(cha)):
                        moves.append(cha)
        return moves

    def get_around(self, pos):
        startx, starty = pos
        positions = []
        positions.append((startx + 1, starty))
        positions.append((startx, starty + 1))
        positions.append((startx - 1, starty))
        positions.append((startx, starty - 1))
        return positions

    def ring(self, upLeft, downRight):
        squares = []
        cursorX, cursorY = upLeft
        while cursorX < downRight[0]:
            self.ring_helper(squares, (cursorX, cursorY))
            cursorX = cursorX + 1
        while cursorY < downRight[1]:
            self.ring_helper(squares, (cursorX, cursorY))
            cursorY = cursorY + 1
        while cursorX > upLeft[0]:
            self.ring_helper(squares, (cursorX, cursorY))
            cursorX = cursorX - 1
        while cursorY > upLeft[1]:
            self.ring_helper(squares, (cursorX, cursorY))
            cursorY = cursorY - 1
        return squares

    def ring_helper(self, squares, position):
        attempted_tile = self.gameState.get_tile_at(position)
        if attempted_tile is not None:
            if self.adversary.set_sights(self.gameState.get_tile_at(position)):
                squares.append(position)

    def chase(self, target):
        moves = []
        if manhattan_distance(self.position, target) <= self.adversary.get_speed():
            moves =  [target]
        else:
            x, y = self.position
            right = (x + 1, y)
            left = (x - 1, y)
            up = (x, y - 1)
            down = (x, y + 1)
            diffX, diffY = x - target[0], y - target[1]
            if diffX == 0:
                if diffY > 0:
                    moves.append(up)
                if diffY < 0:
                    moves.append(down)
            elif diffY == 0:
                if diffX > 0:
                    moves.append(left)
                if diffX < 0:
                    moves.append(right)
            elif diffX > 0 and diffY > 0:
                if diffX > diffY:
                    moves.append(left)
                else:
                    moves.append(up)
            elif diffX > 0 and diffY < 0:
                if diffX > diffY:
                    moves.append(left)
                else:
                    moves.append(down)
            elif diffX < 0 and diffY < 0:
                if diffX > diffY:
                    moves.append(right)
                else:
                    moves.append(down)
            elif diffX < 0 and diffY > 0:
                if diffX > diffY:
                    moves.append(right)
                else:
                    moves.append(up)

        return moves

    """
    Calculates manhattan distance
    """

    # This is a stub for testing
    def set_moves(self, moves):
        pass

    def get_adversary(self):
        return self.adversary
