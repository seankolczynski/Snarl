class Character:

    def __init__(self, speed, id, ctype):
        self.speed = speed
        self.ctype = ctype
        self.current_tile = None
        self.inventory = []
        self.exited = False
        self.id = id


    def move(self, tile):
        if tile.get_character() is not None and tile.get_character().get_ctype() != "player":
            if self.current_tile is not None:
                self.current_tile.remove_character()
        else:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            if self.current_tile == None or self.current_tile.get_item_with_name("Exit") == None:
                self.current_tile = tile
                tile.add_character(self)
            else:
                self.exited = True


    # Character
    def get_char_position(self):
        if self.current_tile is not None:
            return self.current_tile.get_position()
        else:
            return None


    def add_to_inventory(self, item):
        self.inventory.append(item)
    
    def get_ctype(self):
        return self.ctype