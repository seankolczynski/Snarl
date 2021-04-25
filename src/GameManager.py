import GameState
from Beings.Hero import Hero
from RuleChecker import RuleChecker
from SimpleState import SimpleState
from Enums.Status import Status
from Beings.Zombie import Zombie
from Beings.Ghost import Ghost
from Enums.CharacterType import CharacterType
from AdversaryDriver import AdversaryDriver
import json
import Common.JSONToLevel as JLevel
import math

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

    def __init__(self, initial_gamestate, server, layout_list):
        self.game = initial_gamestate
        self.ID_to_user_character = {}
        self.rule_checker = RuleChecker(initial_gamestate)
        self.current_status = Status.NOGAME
        self.observers = []
        self.current_level_id = 1
        self.server = server
        self.layout_list = layout_list

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

    def set_starting_level(self, index):
        self.current_level_id = index
        for i in range(index):
            self.move_to_new_level()

    def move_to_new_level(self):
        self.current_status = Status.INPROGRESS
        key_info = None
        if self.game.key_holder is not None:
            key_info = self.game.key_holder
        print(list(map(lambda x: x.name, self.game.exited)))
        print(list(map(lambda x: x.name, self.game.ejected)))
        output = {
            "type": "end-level",
            "key": key_info,
            "exits": list(map(lambda x: x.name, self.game.exited)),
            "ejects": list(map(lambda x: x.name, self.game.ejected))
        }
        self.server.write(json.dumps(output))
        self.game.next_level()
        self.generate_adversaries()

    def generate_adversaries(self):
        curr_floor = self.game.get_current_floor_index() + 1
        for player in self.game.players:
            self.game.move_character(player, self.game.get_random_empty_tile().get_position())
        (already_z, already_g) = self.game.get_count_adversary()
        num_zombies = math.floor(curr_floor / 2) + 1 - already_z
        num_ghosts = math.floor((curr_floor - 1) / 2) - already_g
        a_uuid = len(self.ID_to_user_character.keys())
        n = already_g + 1
        for i in range(num_ghosts):
            self.register_player_user(AdversaryDriver(str(n) + " Ghost", CharacterType.GHOST, a_uuid))
            a_uuid += 1
            n += 1
        n = already_z + 1
        for i in range(num_zombies):
            self.register_player_user(AdversaryDriver(str(n) + " Zombie", CharacterType.ZOMBIE, a_uuid))
            a_uuid += 1
            n += 1
        new_id_to_char_dict = {}
        for key in self.ID_to_user_character.keys():
            new_id_to_char_dict[key] = self.ID_to_user_character[key][1]
        self.rule_checker.add_characters(new_id_to_char_dict)
        for adv in self.game.get_adversaries():
            while True:
                target = self.game.get_random_empty_tile()
                if adv.fit_the_bill(target):
                    adv.move(target)
                    break

    """
    User -> Void
    Registers the given User into the game.
    Side Effects: Creates character that user will control, adds character to game. Adds user and character to dictionaries
    """

    def register_player_user(self, user):
        id = user.get_id()
        ctype = user.get_type()
        if id in self.ID_to_user_character.keys():
            raise ConnectionError("User ID Taken")
        else:
            if isinstance(user, AdversaryDriver):
                newly_created_character = user.get_adversary()
            else:
                newly_created_character = self.create_new_character(ctype, id, user.get_name())
            self.ID_to_user_character[id] = (user, newly_created_character)
            if ctype == CharacterType.PLAYER:
                self.add_player(newly_created_character)
            else:
                self.add_adversary(newly_created_character)

    def register_observer(self, observer):
        self.observers.append(observer)

    """
    Initialize the game and maintains the loop that keeps it running
    """

    def start_game(self):
        self.generate_adversaries()
        self.update_gamestate()
        self.init_Rule_Checker()
        self.current_status = Status.INPROGRESS
        numLevels = self.game.get_num_levels()
        current_level = self.current_level_id
        while current_level <= numLevels and self.current_status != Status.LOST:
            self.run_level()
            if self.current_status == Status.WON:
                if current_level < numLevels:
                    self.move_to_new_level()
                    self.server.start_new_level(current_level + 1)
                current_level = current_level + 1
                self.update_gamestate()
        if self.current_status == Status.WON:
            print("You won!")
        elif self.current_status == Status.LOST:
            print("Lost on level " + str(current_level))
        self.end_game_stats()
        # self.server.close()

    def run_level(self):
        current_character_turn = 0
        while self.current_status == Status.INPROGRESS or self.current_status == Status.INPROGRESSWON:
            if self.rule_checker.character_alive(self.ID_to_user_character[current_character_turn][1]):
                self.take_turn(current_character_turn), current_character_turn
                self.current_status = self.rule_checker.getGameStatus()
            current_character_turn = (current_character_turn + 1) % len(self.ID_to_user_character)

    def end_game_stats(self):
        key_dict, exit_dict, eject_dict = self.game.get_stats()
        final_stats = {}
        get_name = (lambda x: self.ID_to_user_character[x][1].get_name())
        for user in self.ID_to_user_character.keys():
            if self.ID_to_user_character[user][1].get_ctype() == CharacterType.PLAYER:
                final_stats[user] = (key_dict[user], exit_dict[user], eject_dict[user])
        final_stats = {k: v for k, v in sorted(final_stats.items(), key=lambda item: item[1])}
        score_list = []
        for user in final_stats.keys():
            score_list.append(
                {
                    "type": "player-score",
                    "name": get_name(user),
                    "exits": final_stats[user][1],
                    "keys": final_stats[user][0],
                    "ejected": final_stats[user][2]
                }
            )
            # print(get_name(user) + " exited " + str(final_stats[user][1]) + " times and picked up " + str(final_stats[user][0]) + " keys" )
        output = {
            "type": "end-game",
            "scores": score_list
        }
        self.server.write(json.dumps(output))

    def get_end_game_stats(self):
        key_dict, exit_dict, eject_dict = self.game.get_stats()
        final_stats = {}
        get_name = (lambda x: self.ID_to_user_character[x][1].get_name())
        for user in self.ID_to_user_character.keys():
            if self.ID_to_user_character[user][1].get_ctype() == CharacterType.PLAYER:
                final_stats[user] = (key_dict[user], exit_dict[user], eject_dict[user])
        final_stats = {k: v for k, v in sorted(final_stats.items(), key=lambda item: item[1])}
        score_list = []
        for user in final_stats.keys():
            score_list.append(
                {
                    "type": "player-score",
                    "name": get_name(user),
                    "exits": final_stats[user][1],
                    "keys": final_stats[user][0],
                    "ejected": final_stats[user][2]
                }
            )
            # print(get_name(user) + " exited " + str(final_stats[user][1]) + " times and picked up " + str(final_stats[user][0]) + " keys" )
        return score_list

    def get_ID_to_user_character(self):
        return self.ID_to_user_character

    def leaderboard_stats(self, already):
        key_dict, exit_dict, eject_dict = self.game.get_stats()
        final_stats = {}
        get_name = (lambda x: self.ID_to_user_character[x][1].get_name())
        for user in self.ID_to_user_character.keys():
            if self.ID_to_user_character[user][1].get_ctype() == CharacterType.PLAYER:
                final_stats[user] = (key_dict[user], exit_dict[user], eject_dict[user])
        final_stats = {k: v for k, v in sorted(final_stats.items(), key=lambda item: item[1])}
        score_list = []
        for user in final_stats.keys():
            score_list.append(
                {
                    "type": "player-score",
                    "name": get_name(user),
                    "exits": final_stats[user][1],
                    "keys": final_stats[user][0],
                    "ejected": final_stats[user][2]
                }
            )
            # print(get_name(user) + " exited " + str(final_stats[user][1]) + " times and picked up " + str(final_stats[user][0]) + " keys" )
        output = {
            "type": "leaderboard",
            "scores": score_list + already
        }
        self.server.write(json.dumps(output))
    """
    int -> JSON
    Executes a single turn the user whose turn it currently is. This includes receiving moves until one is approved, 
    executing the move, and updating all users of the new state.
    Also provides a JSON update of what occurred on the turn
    """

    def take_turn(self, turn_index):
        response = None
        current_character = self.ID_to_user_character[turn_index][1]
        current_user = self.ID_to_user_character[turn_index][0]
        move = None
        while True and current_character.is_alive() and not current_character.exited:
            try:
                move = current_user.request_move()
            except ValueError:
                return "Done"
            except Exception:
                return
            if self.rule_checker.validateMove(turn_index, move):
                break
            response = (move, {"success": False, "message": "Invalid", "detail": ""})
            self.give_result(response)
        if move is None:
            response = ((move, {"success": True, "message": "OK", "detail": ""}))
            self.give_result(response)
            return response
        response = (move, self.game.move_character(current_character, move))
        self.give_result(response)
        self.update_gamestate()
        return response

    def give_result(self, result):
        if result is None or result[1] is None or result[1]['message'] is None:
            pass
        else:
            for user in self.ID_to_user_character.keys():
                self.ID_to_user_character[user][0].transmit_message(result[1]['detail'])

    """
    Void
    Updates all players on the most recent version of the game
    """

    def update_gamestate(self):
        for user in self.ID_to_user_character.keys():
            userPos = self.ID_to_user_character[user][1].get_char_position()
            self.ID_to_user_character[user][0].update_state(self.game, userPos)
        for observer in self.observers:
            observer.update_state(SimpleState(self.game.get_current_floor().grid), (0, 0))

    def player_message(self, message):
        for user in self.ID_to_user_character.values():
            user[0].transmit_message(message)

    """
    String, int, String -> Character
    Associates player with an ID, returns a new player or new adversary
    """

    def create_new_character(self, type, id, name):
        if type == CharacterType.PLAYER:
            return Hero(2, id, name)
        elif type == CharacterType.ZOMBIE:
            return Zombie(id, name)
        elif type == CharacterType.GHOST:
            return Ghost(id, name)

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
        self.ID_to_user_character = {}
        self.game = GameState.GameState([])