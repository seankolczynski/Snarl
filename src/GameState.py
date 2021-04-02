from Structures.Tile import Tile, WallTile
from Status import Status
from random import randrange
import sys
# sys.path.append("./Monsters")
# sys.path.append("./Enums")
# from Zombie import Zombie
# from Ghost import Ghost
# from CharacterType import CharacterType
import math

class GameState:

    # For when we have to create random levels on the fly
    # def __init__(self):
    #     self.dungeon = []
    #
    #     ## self.generateGame()

    # Must have one pre-generated level, or error will throw
    def __init__(self, dungeon):
        if len(dungeon) < 1:
            raise ValueError("No floors were given")
        self.dungeon = dungeon
        self.current_floor_index = 0
        self.current_floor = self.dungeon[self.current_floor_index]
        self.players = []
        self.adversaries = []
        self.start_player_position = self.current_floor.rooms[0].upperLeft
        self.start_adversary_position = self.current_floor.rooms[len(self.current_floor.rooms) - 1].upperLeft
        self.unlocked = True
        self.exited = []
        self.ejected = []
        self.current_status = Status.INPROGRESS
    
    def get_random_empty_tile(self):
        current_floor = self.get_current_floor()
        (row, cols) = current_floor.get_row_and_cols()
        for i in range(9223372036854775807):
            rando_tile_pos = (randrange(row-1), randrange(cols-1))
            rando_tile = current_floor.get_tile_at(rando_tile_pos)
            if not isinstance(rando_tile, WallTile) and rando_tile.get_character() == None and rando_tile.get_items() == []:
                return rando_tile
        raise ValueError("Level given does not support a character being placed")

    def move_to_new_level(self):
        self.current_floor_index += 1
        self.adversaries = []
        for player in self.players:
            self.move_character(player, self.get_random_empty_tile()) 
        num_zombies =  math.floor(self.current_floor_index / 2) + 1
        num_ghosts = math.floor((self.current_floor_index  - 1) / 2)
        a_uuid = 100
        n = 0
        for i in range(num_ghosts):
            self.add_adversary(Ghost(1, a_uuid, str(n) + " Ghost", CharacterType.Ghost))
            a_uuid += 1
            n += 1 
        n = 0
        for i in range(num_ghosts):
            self.add_adversary(Zombie(1, a_uuid, str(n) + " Zombie", CharacterType.Zombie))
            a_uuid += 1
            n += 1 
        

    def add_player(self, player):
        # if len(self.players) == 4:
        #     raise UserWarning("No more than 4 players can play at one time")
        # start = self.current_floor.rooms[0]
        # offX, offY = self.start_player_position
        # self.players.append(player)
        # tile = self.current_floor.grid[offX][offY]
        # while type(tile) != Tile or tile.character is not None or tile.room is not start:
        #     offX = offX + 1
        #     if offX > start.upperLeft[0] + start.width:
        #         offX = start.upperLeft[0]
        #         offY = offY + 1
        #     tile = self.current_floor.grid[offX][offY]
        self.move_character(player, self.get_random_empty_tile())

    def add_adversary(self, adversary):
        # start = self.current_floor.rooms[len(self.current_floor.rooms) - 1]
        # offX, offY = self.start_adversary_position
        # self.adversaries.append(adversary)
        # tile = self.current_floor.grid[offX][offY]
        # while type(tile) != Tile or tile.character is not None or tile.room is not start:
        #     offX = offX + 1
        #     if offX > start.upperLeft[0] + start.width:
        #         offX = start.upperLeft[0]
        #         offY = offY + 1
        #     tile = self.current_floor.grid[offX][offY]
        # adversary.move(tile)
        adversary.move(self.get_random_empty_tile())

    """
    If the item is a key, the level becomes locked
    """
    def add_item(self, item, pos):
        if item == "key" or item == "Key":
            self.unlocked = False
        self.current_floor.place_item(item, pos)

    def move_character(self, character, pos):
        destination = self.current_floor.grid[pos[0]][pos[1]]
        if not isinstance(destination, WallTile):
            message = character.move(destination)
            if message is not None and "Ejected" in message['message']:
                self.ejected.append(character)
                self.update_status()
            # Checks if the player just moved to the exit
            if not self.unlocked:
                self.unlocked = self.current_floor.check_if_unlocked()
            if self.unlocked and destination == self.current_floor.get_exit():
                self.exited.append(character)
                self.update_status()
                destination.remove_character()
                return {"success": True, "message": "Exited"}
            return message
        else:
            return {"success": False, "message": "WallTile"}

    def move_player_via_id(self, id, pos):
        return self.move_character(self.players[id], pos)

    def draw(self):
        self.current_floor.draw()

    def get_current_floor(self):
        return self.current_floor

    def get_unlocked(self):
        return self.unlocked

    def get_items(self):
        return self.current_floor.get_items()

    def get_players(self):
        return self.players

    def get_exit(self):
        return self.current_floor.get_exit()

    def set_exit(self, pos):
        self.current_floor.set_exit(pos)

    def get_adversaries(self):
        return self.adversaries

    def unlock(self):
        self.unlocked = True

    def update_status(self):
        dead = len(self.ejected)
        escaped = len(self.exited)
        total_players = len(self.players)
        if dead == total_players:
            self.current_status = Status.LOST
        elif escaped + dead == total_players:
            self.current_status = Status.WON
        elif escaped > 0:
            self.current_status = Status.INPROGRESSWON

    def get_status(self):
        return self.current_status


    def get_intermediate_state(self):
        acc = ""
        acc += "Players: "
        for player in self.players:
            acc += str(player.get_char_position()) + " "
        acc += "\nAdversaries: "
        for adv in self.adversaries:
            acc += str(adv.get_char_position()) + " "
        acc += "\nExit Positions: "
        for level in self.dungeon:
            acc += str(level.get_exit().get_position()) + " "
        return acc