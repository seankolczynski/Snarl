import sys
from enum import Enum
sys.path.append("../src/")

class CharacterType(Enum):
    PLAYER = "Player"
    ZOMBIE = "Zombie"
    GHOST = "Ghost"


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
    if ctype == CharacterType.ZOMBIE:
        return "Z"
    if ctype == CharacterType.GHOST:
        return "G"


