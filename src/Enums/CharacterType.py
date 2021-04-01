from enum import Enum
from Player import Player
from Monsters.Zombie import Zombie
from Monsters.Ghost import Ghost

class CharacterType(Enum):
    PLAYER = Player
    ZOMBIE = Zombie
    GHOST = Ghost

    def reverse_translate(self, ctype):
        if ctype == "player" or ctype == "Player":
            return self.PLAYER
        elif ctype == "zombie" or ctype == "Zombie":
            return self.ZOMBIE
        elif ctype == "ghost" or ctype == "Ghost":
            return self.GHOST

    def make_of_type(self, name, ctype, ID):
        kind = self.reverse_translate(ctype)
        if kind is Player:
            return Player(2, ID, name)
        elif kind is Zombie:
            return Zombie(1, ID, name, CharacterType.ZOMBIE)
        elif kind is Ghost:
            return Ghost(1, ID, name, CharacterType.GHOST)

