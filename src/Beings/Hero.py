from Beings.Character import Character
from Enums.CharacterType import CharacterType

class Hero (Character):

    def __init__(self, speed, id, name):
        super().__init__(speed, id, name, CharacterType.PLAYER, 2)

    def move(self, tile):
        occupant = tile.get_character()
        if occupant is None or occupant == self:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.current_tile = tile
            message = tile.add_character(self)
            return message
        elif occupant.get_ctype() != CharacterType.PLAYER:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.alive = False
            message = {"success": True, "message": "Ejected by " + occupant.get_name()}
            return message
        else:
            message = {"success": False, "message": "Occupied by another player"}
            return message

    def kill(self):
        self.alive = False
        self.current_tile.remove_character()
        self.current_tile = None

    def resurrect(self):
        self.alive = True
        self.exited = False