import json

from Floor import Floor
import Character
from Tile import Tile, WallTile

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
        self.unlocked = False

    def add_player(self, player):
        if len(self.players) == 4:
            raise UserWarning("No more than 4 players can play at one time")
        start = self.current_floor.rooms[0]
        offX, offY = self.start_player_position
        self.players.append(player)
        tile = self.current_floor.grid[offX][offY]
        while type(tile) != Tile or tile.character is not None or tile.room is not start:
            offX = offX + 1
            if offX > start.upperLeft[0] + start.width:
                offX = start.upperLeft[0]
                offY = offY + 1
            tile = self.current_floor.grid[offX][offY]
        self.move_character(player, tile.get_position())

    def add_adversary(self, adversary):
        start = self.current_floor.rooms[len(self.current_floor.rooms) - 1]
        offX, offY = self.start_adversary_position
        self.adversaries.append(adversary)
        tile = self.current_floor.grid[offX][offY]
        while type(tile) != Tile or tile.character is not None or tile.room is not start:
            offX = offX + 1
            if offX > start.upperLeft[0] + start.width:
                offX = start.upperLeft[0]
                offY = offY + 1
            tile = self.current_floor.grid[offX][offY]
        adversary.move(tile)

    def add_item(self, item, pos):
        self.current_floor.place_item(item, pos)

    def move_character(self, character, pos):
        destination = self.current_floor.grid[pos[0]][pos[1]]
        if not isinstance(destination, WallTile):
            message = character.move(destination)
            # Checks if the player just moved to the exit
            if not self.unlocked:
                self.unlocked = self.current_floor.check_if_unlocked()
            if self.unlocked and destination == self.current_floor.get_exit():
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

    def get_adversaries(self):
        return self.adversaries

    def unlock(self):
        self.unlocked = True

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