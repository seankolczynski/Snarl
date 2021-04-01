from Monsters.Adversary import Adversary
from Enums.CharacterType import CharacterType
from Structures.Tile import WallTile

class Ghost(Adversary):

    def default_moves(self, position, map):
        default = []
        immediate_vicinity = self.get_around(position)
        for spot in immediate_vicinity:
            target = map.get_tile_at(spot)


    def set_sights(self, tile):
        chara = tile.get_character()
        return (chara is not None and chara.get_ctype() == CharacterType.PLAYER) or isinstance(tile, WallTile)

    def prioritize(self, stuff, lay):
        play_square = []
        wall_square = []
        for position in stuff:
            tile = lay[position[0]][position[1]]
            if tile.get_character() is not None and tile.get_character().get_ctype() == CharacterType.PLAYER:
                play_square.append(position)
            elif isinstance(tile, WallTile):
                wall_square.append(position)
        ordered = []
        for person in play_square:
            ordered.append(person)
        for wall in wall_square:
            ordered.append(wall)
        return ordered




