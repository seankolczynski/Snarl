class Character:

    def __init__(self, speed, ctype):
        self.speed = speed
        self.ctype = ctype
        self.current_tile = None
        self.inventory = []
        self.exited = False


    def move(self, tile):
        if tile.get_character().get_ctype() == "Player" or tile.get_character().get_ctype() == None  : 
            if self.current_tile is not None:
                self.current_tile.remove_character()
            if self.current_tile.get_item_with_name("Exit") == None: 
                self.current_tile = tile
                tile.add_character(self)
            else:
                self.exited = True
        else:
           if self.current_tile is not None:
                self.current_tile.remove_character() 

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