from Monsters.Adversary import Adversary
from Structures.Tile import Tile, ExitTile


class Zombie(Adversary):

    def default_moves(self, position, map):
        default = []
        immediate_vicinity = self.get_around(position)
        for spot in immediate_vicinity:
            target = map.get_tile_at(spot)
            if (isinstance(target, Tile) or isinstance(target, ExitTile)) and not target.get_room().door_at(
                    target) and not isinstance(target.get_character(), Adversary):
                default.append(target)
        default.append(position)
        return default


