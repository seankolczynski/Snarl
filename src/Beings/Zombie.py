import random

from Beings.Adversary import Adversary
from Structures.Tile import Tile, ExitTile
from Enums.CharacterType import CharacterType


class Zombie(Adversary):

    def __init__(self, id, name):
        super().__init__(1, id, name, CharacterType.ZOMBIE, 3)

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

    def fit_the_bill(self, target_tile):
        return target_tile is not None and (isinstance(target_tile, Tile) or isinstance(target_tile, ExitTile)) and not target_tile.is_door() and not isinstance(target_tile.get_character(), Adversary)

