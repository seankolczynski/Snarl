from Enums.CharacterType import CharacterType
import random

class AdversaryDriver:

    def __init__(self, name, type, ID, moves):
        self.adversary = CharacterType.make_of_type(name, type, ID)
        self.layout = None
        self.move_sequence = moves
        self.ID = ID
        self.type = type
        self.gameState = None
        self.name = name
        self.position = None
        self.vision = 4
        self.moveSpeed = 1
        self.defaults = []

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
        if pos != self.position:
            self.position = pos
            self.get_defaults()
        if pos is not None:
            self.render(pos)
            new_options = self.pick_move()
            if len(new_options) == 0:
                new_options = self.defaults
                new_options.append(self.position)
            else:
                for d in self.defaults:
                    new_options.append(d)
                new_options.append(self.position)


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


    def pick_move(self):
        sight = self.gameState.render_in_range(self.position, self.vision) ##TODO could make sight a field of AdversaryUser
        radius_view = []
        radius = 1
        moves = []
        while radius <= self.vision and len(radius_view) == 0:
            upLeft = (self.position[0] - radius, self.position[1] - radius)
            bottomRight = (self.position[0] + radius, self.position[1] + radius)
            radius_view = self.ring(upLeft, bottomRight, sight)
            radius = radius + 1
        if len(radius_view) > 0:
            target = radius_view[random.randint(0, len(radius_view) - 1)]
            moves = self.chase(target)
        return moves


    def get_around(self, pos):
        startx, starty = pos
        positions = []
        positions.append((startx + 1, starty))
        positions.append((startx, starty + 1))
        positions.append((startx - 1, starty))
        positions.append((startx, starty - 1))
        return positions

    def ring(self, upLeft, downRight, sight):
        squares = []
        cursorX, cursorY = upLeft
        while cursorX < downRight[0]:
            if(self.set_sights(sight[cursorX][cursorY])):
                squares.append((cursorX, cursorY))
            cursorX = cursorX + 1
        while cursorY < downRight[1]:
            if (self.set_sights(sight[cursorX][cursorY])):
                squares.append((cursorX, cursorY))
            cursorY = cursorY + 1
        while cursorX > upLeft[0]:
            if (self.set_sights(sight[cursorX][cursorY])):
                squares.append((cursorX, cursorY))
            cursorX = cursorX - 1
        while cursorY > upLeft[1]:
            if (self.set_sights(sight[cursorX][cursorY])):
                squares.append((cursorX, cursorY))
            cursorY = cursorY - 1
        return squares

    def set_sights(self, tile):
        chara = tile.get_character()
        return chara is not None and chara.get_ctype() == CharacterType.PLAYER

    def chase(self, target):
        moves = []
        if self.manhattan_distance(self.position, target) <= self.moveSpeed:
            return [target]
        else:
            x, y = self.position
            diffX, diffY = x - target[0], y - target[1]
            if diffX == 0:
                if diffY > 0:
                    moves.append((x, y - 1))
                if diffY < 0:
                    moves.append((x, y + 1))
            elif diffY == 0:
                if diffX > 0:
                    moves.append((x - 1, y))
                if diffX < 0:
                    moves.append((x + 1, y))
            elif diffX > 0 and diffY > 0:
                if diffX > diffY:
                    moves.append((x - 1, y))
                else:
                    moves.append((x, y - 1))
            elif diffX > 0 and diffY < 0:
                if diffX > diffY:
                    moves.append((x - 1, y))
                else:
                    moves.append((x, y + 1))
            elif diffX < 0 and diffY < 0:
                if diffX > diffY:
                    moves.append((x + 1, y))
                else:
                    moves.append((x, y + 1))
            elif diffX < 0 and diffY > 0:
                if diffX > diffY:
                    moves.append((x + 1, y))
                else:
                    moves.append((x, y - 1))
            return moves

    """
    Calculates manhattan distance
    """
    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x2 - x1) + abs(y2 - y1)

    # This is a stub for testing
    def set_moves(self, moves):
        pass

    def get_defaults(self):
        around = self.get_around(self.position)
        random.shuffle(around)
        around.append(self.position)
        return around

