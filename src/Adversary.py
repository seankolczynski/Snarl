from Character import Character


class Adversary (Character):

    def __init__(self, speed, type):
        super().__init__(speed, 0, type)