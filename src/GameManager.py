import GameState
from Player import Player
from Adversary import Adversary
from RuleChecker import RuleChecker
from SimpleState import SimpleState

"""
The cycle of the game manager:
- Designate whose turn it is
- Indicate to proper user  that it is there turn, expecting return
- Receive Move
- Validate Move
- Execute Move
- Update all players on new state

Outside of this loop, it also needs to start and end the game
"""


class GameManager:

    def __init__(self, initial_gamestate):
        # TODO Add Websocket logic???
        self.game = initial_gamestate
        self.ID_to_char = {}
        self.ID_to_user = {}
        self.rule_checker = None

    # Adds a player to the gamestate
    def add_player(self, player):
        self.game.add_player(player)

    def add_adversary(self, adversary):
        self.game.add_adversary(adversary)

    """
    User -> Void
    Registers the given User into the game.
    Side Effects: Creates character that user will control, adds character to game. Adds user and character to dictionaries
    """
    def register_player_user(self, user):
        id = user.get_id()
        type = user.get_type()
        if id in self.ID_to_char.keys() or id in self.ID_to_user.keys():
            raise ConnectionError("User ID Taken")
        else:
            newly_created_character = self.create_new_character(type, id, user.get_name())
            self.ID_to_user[id] = user
            self.ID_to_char[id] = newly_created_character
            if type == "player":
                self.add_player(newly_created_character)
            else:
                self.add_adversary(newly_created_character)
    """
    Initialize the game and maintains the loop that keeps it running
    """
    def start_game(self):
        self.add_Rule_Checker()
        current_character_turn = 0
        while True:
            self.take_turn(current_character_turn)
            current_character_turn = current_character_turn + 1

    """Executes a single turn the user whose turn it currently is. This includes receiving moves until one is approved, 
    executing the move, and updating all users of the new state"""
    def take_turn(self, turn_index):
        responses = []
        current_character = self.ID_to_char[turn_index]
        current_user = self.ID_to_user[turn_index]
        while True:
            try:
                move = current_user.request_move()
            except ValueError:
                return "Done"
            if self.rule_checker.validateMove(turn_index, move):
                break
            responses.append((move, "Invalid"))
        if move is None:
            responses.append((move, {"success": True, "message": "OK"}))
            return responses
        responses.append((move, self.game.move_character(current_character, move)))
        self.update_gamestate()
        return responses

    def update_gamestate(self):
        for user in self.ID_to_user.keys():
            userPos = self.ID_to_char[user].get_char_position()
            self.ID_to_user[user].update_state(SimpleState(self.game.get_current_floor().grid), userPos)

    # Associates player with an ID, that returns a new player or new adversary
    def create_new_character(self, type, id, name):
        if type == "player":
            return Player(2, id, name)
        else:
            return Adversary(1, id, type, name)

    def add_Rule_Checker(self):
        self.rule_checker = RuleChecker(self.game, self.ID_to_char)


    #The game is over, and this method will reset to the initial gamestate
    def reset(self):
        self.rule_checker = None
        self.ID_to_char = {}
        self.game = GameState.GameState([])



