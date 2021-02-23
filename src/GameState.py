import Floor
import Character
import Tile

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


    def add_player(self, player):
        start = self.current_floor.rooms[0]
        offX, offY = self.start_player_position
        self.players.append(player)
        tile = self.current_floor.grid[offX][offY]
        while type(tile) != Tile.Tile or tile.character is not None or tile.room is not start:
            offX = offX + 1
            if offX > start.width:
                offX = start.upperLeft[0]
                offY = offY + 1
            tile = self.current_floor.grid[offX][offY]
        player.move(tile)
        


    def add_adversary(self, adversary):
        start = self.current_floor.rooms[len(self.current_floor.rooms)]
        offX, offY = self.start_player_position
        self.adversaries.append(adversary)
        tile = self.current_floor.grid[offX][offY]
        while type(tile) != Tile.Tile or tile.character is not None or tile.room is not start:
            offX = offX + 1
            if offX > start.width:
                offX = start.upperLeft[0]
                offY = offY + 1
            tile = self.current_floor.grid[offX][offY]
        adversary.move(tile)

