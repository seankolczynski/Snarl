import Floor
import Character

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
        self.start_player_position = (0, 0)
        self.start_adversary_position = (0, 0)


    def add_player(self, player):
        self.players.append(player)
        upper_left_room = self.current_floor.rooms[0]
        offX, offY = upper_left_room.upperLeft
        while tile.character is None:
            try:
                tile = self.current_floor.grid[offX][offY]
            except:
                if offY >= len(self.current_floor.grid):
                    raise ValueError("Start Room is full")
                elif offX >= len(self.current_floor.grid[offX]):
                    offX = 0
                    offY = offY + 1
                else:
                    offX = offX + 1
        player.move(tile)



    def add_adversary(self, adversary):
        self.adversaries.append(adversary)
        upper_left_room = self.current_floor.rooms[len(self.current_floor.rooms) - 1]
        offX, offY = upper_left_room.upperLeft
        while tile.character is None:
            try:
                tile = self.current_floor.grid[offX][offY]
            except:
                if offY >= len(self.current_floor.grid):
                    raise ValueError("Start Room is full")
                elif offX >= len(self.current_floor.grid[offX]):
                    offX = 0
                    offY = offY + 1
                else:
                    offX = offX + 1
        adversary.move(tile)

