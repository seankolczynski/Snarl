from Enums.CharacterType import CharacterType


class Character:

    def __init__(self, speed, id, name, ctype, FOV_radius):
        self.speed = speed
        self.ctype = ctype
        self.name = name
        self.current_tile = None
        self.inventory = []
        self.exited = False
        self.id = id
        self.alive = True
        self.FOV_radius = FOV_radius


    def move(self, tile):
        occupant = tile.get_character()
        if occupant is None or occupant == self:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.current_tile = tile
            message = tile.add_character(self)
            return message
        elif occupant.get_ctype() != CharacterType.PLAYER:
            if self.current_tile is not None:
                self.current_tile.remove_character()
            self.alive = False
            message = {"success": True, "message": "Ejected by " + occupant.get_name(), "detail": ""}
            return message
        else:
            message = {"success": False, "message": "Occupied by another player", "detail": ""}
            return message


    # Character
    def get_char_position(self):
        if self.current_tile is not None and self.alive:
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

    def get_id(self):
        return self.id

    def is_alive(self):
        return self.alive

