from abc import ABC
import random
from Character import Character
from Enums.CharacterType import CharacterType


class Adversary(Character):

    def __init__(self, speed, id, name, ctype):
        super().__init__(speed, id, name, ctype)
        self.ID = id
        self.type = ctype
        self.name = name

    def get_id(self):
        return self.ID

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name




