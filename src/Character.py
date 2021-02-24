class Character:

    def __init__(self, speed):
        self.speed = speed
        self.current_tile = None
        self.inventory = []


    def move(self, tile):
        if self.current_tile is not None:
            self.current_tile.remove_character()
            self.current_tile = tile
            tile.add_character(self)
        else:
            self.current_tile = tile

    # Character
    def get_char_position(self):
        if self.current_tile is not None:
            return self.current_tile.get_position()
        else:
            return None


    def add_to_inventory(self, item):
        self.inventory.append(item)