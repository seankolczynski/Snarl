from Character import Character


class Player (Character):

    def __init__(self, speed, id):
        super().__init__(speed, id, "player")
