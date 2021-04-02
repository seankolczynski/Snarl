from Character import Character
from Enums.CharacterType import CharacterType


class Hero (Character):

    def __init__(self, speed, id, name):
        super().__init__(speed, id, name, CharacterType.PLAYER, 2)

