import GameState
from Player import Player
from Adversary import Adversary

class GameManager:

    def __int__(self, initial_gamestate):
        # TODO Add Websocket logic???
        self.game = GameState.GameState([])
        self.ID_to_char = {}

        self.rule_checker = None

    # Adds a player to the gamestate
    def add_player(self, player):
        self.game.add_player(player)

    def add_adversary(self, adversary):
        self.game.add_adversary(adversary)


    # Associates player with an ID, that returns a new player or new adversary
    # TODO All this
    def create_new_character(self, type, ID):
        if type == "Player":
            # TODO Check for Unique IDs
        else:
            # Adversary yooo

    def add_Rule_Checker(self):
        self.rule_checker = RuleChecker.RuleChecker(self.game, self.ID_to_char)


    #The game is over, and this method will reset to the initial gamestate
    def reset(self):
        self.rule_checker = None
        self.ID_to_char = {}
        self.game = GameState.GameState([])


    def move(self, pos, playerID):
        player = self.ID_to_char[playerID]
        if self.rule_checker.check_move(playerID, pos):
            player.move(pos)
