import GameState
from Player import Player
from Monsters.Adversary import Adversary
from RuleChecker import RuleChecker
from SimpleState import SimpleState
from Status import Status
from Enums.CharacterType import CharacterType
import Enums.CharacterType as CT

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
        self.game = initial_gamestate
        self.ID_to_user_character = {}
        self.rule_checker = RuleChecker(initial_gamestate)
        self.current_status = Status.NOGAME
        self.observers = []

    """
    Player -> Void
    Adds the given player to our gamestate
    """
    def add_player(self, player):
        self.game.add_player(player)

    """
    Adversary -> Void
    Adds the given adversary to the gamestate
    """
    def add_adversary(self, adversary):
        self.game.add_adversary(adversary)

    """
    User -> Void
    Registers the given User into the game.
    Side Effects: Creates character that user will control, adds character to game. Adds user and character to dictionaries
    """
    def register_player_user(self, user):
        id = user.get_id()
        type = CT.reverse_translate(user.get_type())
        if id in self.ID_to_user_character.keys():
            raise ConnectionError("User ID Taken")
        else:
            newly_created_character = self.create_new_character(type, id, user.get_name())
            self.ID_to_user_character[id] = (user, newly_created_character)
            if type == CharacterType.PLAYER:
                self.add_player(newly_created_character)
            else:
                self.add_adversary(newly_created_character)

    def register_observer(self, observer):
        self.observers.append(observer)

    """
    Initialize the game and maintains the loop that keeps it running
    """
    def start_game(self):
        self.init_Rule_Checker()
        current_character_turn = 0
        while self.current_status == Status.INPROGRESS or self.current_status == Status.INPROGRESSWON:
            if self.rule_checker.character_alive(self.ID_to_user_character[current_character_turn][1]):
                self.take_turn(current_character_turn)
                self.current_status = self.rule_checker.getGameStatus()
            current_character_turn = (current_character_turn + 1) % len(self.ID_to_user_character)


    """
    int -> JSON
    Executes a single turn the user whose turn it currently is. This includes receiving moves until one is approved, 
    executing the move, and updating all users of the new state.
    Also provides a JSON update of what occurred on the turn
    """
    def take_turn(self, turn_index):
        responses = []
        current_character = self.ID_to_user_character[turn_index][1]
        current_user = self.ID_to_user_character[turn_index][0]
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

    """
    Void
    Updates all players on the most recent version of the game
    """
    def update_gamestate(self):
        for user in self.ID_to_user_character.keys():
            userPos = self.ID_to_user_character[user][1].get_char_position()
            self.ID_to_user_character[user][0].update_state(SimpleState(self.game.get_current_floor().grid), userPos)
        for observer in self.observers:
            observer.update_state(SimpleState(self.game.get_current_floor().grid))

    """
    String, int, String -> Character
    Associates player with an ID, returns a new player or new adversary
    """
    def create_new_character(self, type, id, name):
        if type == "player":
            return Player(2, id, name)
        else:
            return Adversary(1, id, type, name)

    """
    Genereates a new Rule Checker based on the current gamestate
    """
    def init_Rule_Checker(self):
        just_chars = []
        for pair in self.ID_to_user_character:
            just_chars.append(self.ID_to_user_character[pair][1])
        self.rule_checker.add_characters(just_chars)


    """The game is over, and this method will reset to the initial gamestate
    """
    def reset(self):
        self.rule_checker = None
        self.ID_to_char = {}
        self.game = GameState.GameState([])



