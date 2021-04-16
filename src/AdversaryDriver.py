from Enums.CharacterType import CharacterType
from Beings.Hero import Hero
from Beings.Zombie import Zombie
from Beings.Ghost import Ghost
from PlayerUser import PlayerUser


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


class AdversaryDriver(PlayerUser):

    def __init__(self, name, ctype, ID):
        super().__init__(name, ctype, ID)
        self.adversary = make_of_type(name, ctype, ID)
        self.layout = None
        self.move_sequence = []
        self.gameState = None
        self.position = None
        self.vision = self.adversary.FOV_radius
        self.defaults = []

    def get_id(self):
        return self.adversary.get_id()

    def get_type(self):
        return self.adversary.get_type()

    def get_name(self):
        return self.adversary.get_name

    """Called by the GameManager, requests the first of the list of options"""

    def request_move(self):
        if len(self.move_sequence) > 0:
            move = self.move_sequence.pop(0)
            # if move is None:
            #    return self.position
            return move
        else:
            raise ValueError("Out of moves")

    """Called by GameManager, provides our position and the simple gamestate. If position changes (aka we have moved), we update our current surroundings"""
    def update_state(self, gs, pos):
        self.gameState = gs
        if pos != self.position:
            self.position = pos
            self.defaults = self.adversary.default_moves(self.position, self.gameState)
        if pos is not None:
            self.render(pos)
            new_options = self.pick_moves()
            new_options.extend(self.defaults)
            self.move_sequence = new_options


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
