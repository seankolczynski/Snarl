
from enum import Enum

class CharacterType(Enum):
    PLAYER = "player"
    ZOMBIE = "zombie"
    GHOST = "ghost"


def reverse_translate(ctype):
    if ctype == "player" or ctype == "Player":
        return CharacterType.PLAYER
    elif ctype == "zombie" or ctype == "Zombie":
        return CharacterType.ZOMBIE
    elif ctype == "ghost" or ctype == "Ghost":
        return CharacterType.GHOST

def draw(ctype):
    if ctype == CharacterType.PLAYER:
        return "P"
    elif ctype == CharacterType.ZOMBIE:
        return "Z"
    elif ctype == CharacterType.GHOST:
        return "G"
    else:
        return "A"



