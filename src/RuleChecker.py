from queue import Queue

from Tile import Tile, WallTile


class RuleChecker:

    def __init__(self, game, playerIDs):
        self.game = game
        self.playerIDs = playerIDs

    # (Character, Position) -> Boolean
    # given a character and tile, will check the gamestate to see if a move is possible
    def validateMove(self, id, position):
        if position is None:
            return True
        floor = self.game.get_current_floor()
        charact = self.playerIDs[id]
        target = floor.get_tile_at(position)
        current = charact.get_char_position()
        if not isinstance(target, WallTile):
            if self.manhattan_distance(current, target.get_position()) <= charact.get_speed():
                return True
        else:
            return False

    def breadthFirstSearch(self, start_pos, target_pos):
        """Search the shallowest nodes in the search tree first."""
        frontier = []
        explored = []
        # We have to keep a record of the path to each point
        frontier.append((start_pos, []))
        while True:
            # Failed state, could not find end.
            if len(frontier) == 0:
                return []
            # pop next state
            pos, path = frontier.pop()
            explored.append(pos)
            if pos == target_pos:
                return path
            succers = self.get_around(pos)
            for node in succers:
                if not (explored.__contains__(node[0])) and node[0] not in (nextGo[0] for nextGo in
                                                                            frontier) and not isinstance(
                        self.game.get_current_floor().get_tile_at(node[0]), WallTile):
                    nextStep = path + [node[1]]
                    frontier.append((node[0], nextStep))

    """
    Calculates manhattan distance
    """
    def manhattan_distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x2 - x1) + abs(y2 - y1)


    def get_around(self, pos):
        startx, starty = pos
        positions = []
        positions.append((startx + 1, starty))
        positions.append((startx, starty + 1))
        positions.append((startx - 1, starty))
        positions.append((startx, starty - 1))
        return positions

    # uses internal gamestate to check if a game is over
    # this condition is if all players have been defeated
    # def isGameOver():

    # int -> boolean
    # given a floor index checks if floor is completed or not
    # dungeon will look up floor and see if all players are at the exit or not\
    # def IsLevelCompleted(self, index):

    # (Character, Tile) -> Int
    # returns the shortest path it can take given the current dungeon; returns - 1 if not possible
# def shortestPath(self, character, move_to_tile):
