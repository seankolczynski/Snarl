from Beings.Adversary import Adversary
from Enums.CharacterType import CharacterType
from Structures.Tile import WallTile, Tile, ExitTile
import random


class Ghost(Adversary):

    def __init__(self, id, name):
        super().__init__(1, id, name, CharacterType.GHOST, 3)


    def set_sights(self, tile):
        if tile is None:
            return False
        chara = tile.get_character()
        return (chara is not None and chara.get_ctype() == CharacterType.PLAYER) or isinstance(tile, WallTile)

    def prioritize(self, positions, lay):
        play_square = []
        wall_square = []
        for position in positions:
            tile = lay.get_tile_at(position)
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

    def fit_the_bill(self, target_tile):
        return target_tile is not None and not isinstance(target_tile.get_character(), Adversary)

    def special_move(self, floor):
        rooms = floor.rooms
        while True:
            goal_room = random.choice(rooms)
            room_grid = goal_room.layout
            goal_tile = random.choice(random.choice(room_grid))
            occupant = goal_tile.get_character()
            if not isinstance(goal_tile, WallTile) and occupant is None:
                return goal_tile
