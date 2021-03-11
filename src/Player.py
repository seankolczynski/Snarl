from Character import Character


class Player (Character):

    def __init__(self, speed, id, name):
        super().__init__(speed, id, name, "player")
