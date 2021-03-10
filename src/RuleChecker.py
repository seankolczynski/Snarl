class RuleChecker:

    def __int__(self, game, playerIDs):
        self.game = game
        self.playerIDs = playerIDs


    # (Character, Tile) -> Boolean
    # given a character and tile, will check the gamestate to see if a move is possible
    def validateMove(self, id, move_to_tile):

    # uses internal gamestate to check if a game is over
    # this condition is if all players have been defeated
    def isGameOver():

    # int -> boolean
    # given a floor index checks if floor is completed or not
    # dungeon will look up floor and see if all players are at the exit or not\
    def IsLevelCompleted(self, index):

    # (Character, Tile) -> Int
    # returns the shortest path it can take given the current dungeon; returns - 1 if not possible
    def shortestPath(self, character, move_to_tile):
