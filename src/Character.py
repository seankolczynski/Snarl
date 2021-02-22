class Character:

    def __init__(self, speed):
        self.speed = speed
        self.current_tile = None


    def move(self, tile):
        self.current_tile = tile
        tile.add_character(self)

