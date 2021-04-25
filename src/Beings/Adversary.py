import random
from Beings.Character import Character
from Enums.CharacterType import CharacterType
from Structures.Tile import Tile, ExitTile


class Adversary(Character):

    def __init__(self, speed, id, name, ctype, FOV_radius):
        super().__init__(speed, id, name, ctype, FOV_radius)
        self.ID = id
        self.ctype = ctype
        self.name = name

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.ctype

    def get_name(self):
        return self.name

    def default_moves(self, position, map):
        default = []
        immediate_vicinity = self.get_around(position)
        for spot in immediate_vicinity:
            target = map.get_tile_at(spot)
            if self.fit_the_bill(target):
                default.append(spot)
        random.shuffle(default)
        default.append(position)
        return default

    def get_around(self, pos):
        startx, starty = pos
        positions = []
        positions.append((startx + 1, starty))
        positions.append((startx, starty + 1))
        positions.append((startx - 1, starty))
        positions.append((startx, starty - 1))
        return positions

    def set_sights(self, tile):
        chara = tile.get_character()
        return chara is not None and chara.get_ctype() == CharacterType.PLAYER

    def prioritize(self, stuff, lay):
        return stuff

    def fit_the_bill(self, target_tile):
        return target_tile is not None and (isinstance(target_tile, Tile) or isinstance(target_tile, ExitTile)) \
               and not isinstance(target_tile.get_character(), Adversary)

    def move(self, tile):
        occupant = tile.get_character()
        message = None
        if occupant is None or occupant == self:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.current_tile = tile
            message = tile.add_character(self)
            return message
        elif occupant.get_ctype() == CharacterType.PLAYER:
            occupant.kill()
            message = {"success": True, "message": "Ejected player", "detail": "Player " + occupant.get_name() + " was expelled"}
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.current_tile = tile
            tile.add_character(self)
            return message
        else:
            message = {"success": False, "message": "Occupied by another adversary", "detail": ""}
            return message

    def special(self, tile):
        return None