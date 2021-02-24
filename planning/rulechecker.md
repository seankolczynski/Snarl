RuleChecker interface:  {
    
    // self, List<Levels>
    def __init__(self, dungeon):
        Self.dungeon =  dungeon
    
    // (Character, Tile) -> Boolean
    /// given a character and tile, will check the gamestate to see if a move is possible
    Def validateMove(character, move_to_tile):
    
    // uses internal gamestate to check if a game is over
    // this condition is if all players have been defeated
    Def isGameOver()

    // int -> boolean
    // given a floor index checks if floor is completed or not
    // dungeon will look up floor and see if all players are at the exit or not
    Def IsLevelCompleted(int index)

    // (Character, Tile) -> Int
    // returns the shortest path it can take given the current dungeon; returns -1 if not possible
    Def shortestPath(character, move_to_tile)

}

//Explanation
So our main interface will determine if a player is captured by an adversary or picks up an item like a key based on movement. Therefore, using movement we will check if a given player can move to another tile based on what is occupying it. If a player moves to a tile with an item on it, it will pick it up. If a player moves to a square with an adversary or vice versa it will be considered valid and that player will be removed. We will check if a player can move to a given tile by checking the shortest path to that file
