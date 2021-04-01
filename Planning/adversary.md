# Represents a user that is an adversary
Class AdversarUser:


# String, Int ->  AdversaryUser 
# takes in a string representing the adversary type and a unique id to associate with the adversary # user 
# has a list of moves as a class variable representing the list of moves it can make as moves
# and a variable of when its is turn as isTurn
Def init(self,type,Id)


# Void
# gets the id field
Def get_id(self)


# Void
# gets the type field
Def get_typer(self)


# Void
# pops the next move set in the class variable that stores adversary moves 
# this is how we will “make moves from the adversary”
# the game manager will set the moves and then request them by invoking this method
Def request_move(self)


# Gamestate -> Void
# updates the given gamestate by the setting it to the given gamestate 
Def update_gamestate(self, gs)


# List<Positions> -> Void
# sets the list of moves equal to the give list
Def set_moves(self, moves)


# List<Positions> -> Void
# adds a list of moves to the adversary’s list of moves
Def add_moves(self, moves)


# Void -> String
# returns the full level information from the gamestate set in the constructor 
Def getGodView(self)


# Void 
# sets IsTurn class variable to opposite
Def changeIsTurn(self)


# Void -> String
# returns player locations but only if isTurn is true
Def getPlayerLocs(self)


During the game the AdversaryUser will be managed by the GameManager, given its turn when it is ready. It will receive updates via the shared gamestate field in all the AdversaryUser/AdversaryUser objects. It can access its godview at any time.




GameManger ---  Allows when turn to make Move ----> Player/AdversaryUser           GameState
                  --- Requests Move from Player -----------> 
                 < -------- gives Move to game manager 
                      ----------| Checks within Rulechecker if allowed
                       <--------
                          ----------------------------------------------------------------------- Updates move in --->