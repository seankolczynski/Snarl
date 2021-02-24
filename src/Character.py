class Character:

    def __init__(self, speed):
        self.speed = speed
        self.current_tile = None
        self.inventory = []


    def move(self, tile):
        self.current_tile.remove_character()
        self.current_tile = tile
        tile.add_character(self)

    # Character
    def get_char_position(self):
        return self.current_tile.get_position()


    def add_to_inventory(self, item):
        self.inventory.append(item)