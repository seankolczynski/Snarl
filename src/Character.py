import json


class Character:

    def __init__(self, speed, id, name, ctype):
        self.speed = speed
        self.ctype = ctype
        self.name = name
        self.current_tile = None
        self.inventory = []
        self.exited = False
        self.id = id
        self.alive = True


    def move(self, tile):
        occupant = tile.get_character()
        if occupant is None:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.current_tile = tile
            tile.add_character(self)
        elif occupant.get_ctype() != "player":
            if self.current_tile is not None:
                self.current_tile.remove_character()
            return json.dumps({"success": True, "message": "Ejected by " + occupant.get_name()})
        else:
            return json.dumps({"success": False, "message": "Occupied by another player"})


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

    def get_speed(self):
        return self.speed

    def get_name(self):
        return self.name