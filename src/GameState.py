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
            if offX > start.width:
                offX = start.upperLeft[0]
                offY = offY + 1
            tile = self.current_floor.grid[offX][offY]
        player.move(tile)

    def add_adversary(self, adversary):
        start = self.current_floor.rooms[len(self.current_floor.rooms) - 1]
        offX, offY = self.start_adversary_position
        self.adversaries.append(adversary)
        tile = self.current_floor.grid[offX][offY]
        while type(tile) != Tile or tile.character is not None or tile.room is not start:
            offX = offX + 1
            if offX > start.width:
                offX = start.upperLeft[0]
                offY = offY + 1
            tile = self.current_floor.grid[offX][offY]
        adversary.move(tile)

    def add_item(self, item, pos):
        self.current_floor.place_item(item, pos)

    def move_player(self, playerID, pos):
        destination = self.current_floor.grid[pos[0]][pos[1]]
        if not isinstance(destination, WallTile):
            message = self.players[playerID - 1].move(destination)
            # Checks if the player just moved to the exit
            if self.unlocked and destination == self.current_floor.get_exit():
                destination.remove_character()
                return json.dumps({"success": True, "message": "Exited"})
            return message
        else:
            return json.dumps({"success": False, "message": "WallTile"})

    def draw(self):
        self.current_floor.draw()

    def get_current_floor(self):
        return self.current_floor


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
     