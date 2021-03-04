// Abstract interface that will be used  by any active player
class Character:

    //Constructor, standard things for all characters
    // speed is how many movements a character can make
    // current_tile is the Tile a Character is currently on
    // inventory is a list of items
    // view_distance is an int
    def __init__(self, speed, view_distance):
        self.speed = speed
        self.current_tile = None
        self.inventory = [] 
        Self.view_distance = view_distance

     // tile -> void
    //Moves character to the given Tile, if possible
    // Interacts with tiles on move in the given order 
    def move(self, tile):
      
     //   Void -> void
    //Returns character’s current position
    def get_char_position(self):
    
    // item -> void 
   // adds an item to this characters inventory
    def add_to_inventory(self, item):
   

// Player extends Character
from Character import Character

class Player (Character):

    def __init__(self, speed):
        super().__init__(speed)


// We decided that the logic for viewing the surroundings will be in the view class for our MVC architecture. It doesn’t really make sense for the model to want to “see” the surroundings of the player when it is mostly important for the view. If we implemented that function in the Player class for the model it would merge those two together and confuse our architecture. Hopefully by making sure each is separate it can be more extendable for the future.
