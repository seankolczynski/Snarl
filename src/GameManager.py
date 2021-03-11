import GameState
from Player import Player
from Adversary import Adversary
from RuleChecker import RuleChecker

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

    def __int__(self, initial_gamestate):
        # TODO Add Websocket logic???
        self.game = GameState.GameState([])
        self.ID_to_char = {}
        self.ID_to_user = {}
        self.rule_checker = None

    # Adds a player to the gamestate
    def add_player(self, player):
        self.game.add_player(player)

    def add_adversary(self, adversary):
        self.game.add_adversary(adversary)

    def register_player_user(self, user):
        id = user.get_id()
        type = user.get_type()
        if id in self.ID_to_char.keys() or id in self.ID_to_user.keys():
            raise ConnectionError("User ID Taken")
        else:
            newly_created_character = self.create_new_character(type, id, "")
            self.ID_to_user[id] = user
            self.ID_to_char[id] = newly_created_character
            if type == "player":
                self.add_player(newly_created_character)
            else:
                self.add_adversary(newly_created_character)

    def start_game(self):
        self.add_Rule_Checker()
        current_character_turn = 0
        current_character = self.ID_to_char[current_character_turn]
        current_user = self.ID_to_user[current_character_turn]
        while True:
            while True:
                move = current_user.request_move()
                if self.rule_checker.validateMove(current_character_turn, move):
                    break
            self.move(move, current_character_turn)
            self.update_gamestate()
            current_character_turn = ((current_character_turn + 1) % len(self.ID_to_user))
            current_character = self.ID_to_char[current_character_turn]
            current_user = self.ID_to_user[current_character_turn]



    def update_gamestate(self):
        for user in self.ID_to_user.keys():
            self.ID_to_user[user].update_state(self.game)

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


    def move(self, pos, playerID):
        player = self.ID_to_char[playerID]
        if self.rule_checker.check_move(playerID, pos):
            player.move(pos)
