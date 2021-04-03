from Structures.Tile import WallTile, ExitTile
from Enums.Status import Status
from random import randrange
from Enums.CharacterType import CharacterType
from collections import defaultdict
from Beings.Adversary import Adversary


class GameState:

    # For when we have to create random levels on the fly
    # def __init__(self):
    #     self.dungeon = []
    #
    #     ## self.generateGame()

    # Must have one pre-generated level, or error will throw
    def __init__(self, dungeon):
        if len(dungeon) < 1:
            raise ValueError("No floors were given")
        self.dungeon = dungeon
        self.current_floor_index = 0
        self.current_floor = self.dungeon[self.current_floor_index]
        self.players = []
        self.adversaries = []
        self.start_player_position = self.current_floor.rooms[0].upperLeft
        self.start_adversary_position = self.current_floor.rooms[len(self.current_floor.rooms) - 1].upperLeft
        self.exited = []
        self.ejected = []
        self.items = self.current_floor.get_items()
        self.unlocked = self.lock_status()
        self.current_status = Status.INPROGRESS
        self.character_to_exits = defaultdict(int)
        self.character_to_keys = defaultdict(int)

    def get_random_empty_tile(self):
        current_floor = self.get_current_floor()
        (row, cols) = current_floor.get_row_and_cols()
        for i in range(9223372036854775807):
            rando_tile_pos = (randrange(row-1), randrange(cols-1))
            rando_tile = current_floor.get_tile_at(rando_tile_pos)
            if not isinstance(rando_tile, WallTile) and not isinstance(rando_tile, ExitTile) and rando_tile.get_character() is None and rando_tile.get_all_items() == []:
                return rando_tile
        raise ValueError("Level given does not support a character being placed")

    def get_count_adversary(self):
        z_c = 0
        g_c = 0
        for adver in self.get_adversaries():
            if adver.get_ctype() == CharacterType.GHOST:
                g_c += 1
            else:
                z_c += 1
        return(z_c, g_c)
   

    def add_player(self, player):
        self.players.append(player)
        self.move_character(player, self.get_random_empty_tile().get_position())
        self.character_to_exits[player.get_id()] = 0
        self.character_to_keys[player.get_id()] = 0

    def add_adversary(self, adversary):
        self.adversaries.append(adversary)
        self.move_character(adversary, self.get_random_empty_tile().get_position())

    """
    If the item is a key, the level becomes locked
    """
    def add_item(self, item, pos):
        if item == "key" or item == "Key":
            self.unlocked = False
        self.current_floor.place_item(item, pos)

    def move_character(self, character, pos):
        destination = self.current_floor.grid[pos[0]][pos[1]]
        if not isinstance(destination, WallTile):
            message = character.move(destination)
            # Checks if the player just moved to the exit
            if not self.unlocked:
                self.unlocked = self.current_floor.check_if_unlocked()
            if message is not None and "Key" in message['message']:
                print("Player " + character.get_name() + " picked up a key")
                self.character_to_keys[character.get_id()] = self.character_to_keys[character.get_id()] + 1
            if self.unlocked and destination == self.current_floor.get_exit() and character.get_ctype() == CharacterType.PLAYER:
                self.exited.append(character)
                self.character_to_exits[character.get_id()] = self.character_to_exits[character.get_id()] + 1
                self.update_status()
                destination.remove_character()
                print("Player " + character.get_name() + " exited")
                message = {"success": True, "message": "Exited"}

        else:
            if character.get_ctype() == CharacterType.GHOST:
                message = character.move(character.special_move(self.current_floor))
            else:
                message = {"success": False, "message": "WallTile"}
        if isinstance(character, Adversary):
            self.who_died()
        return message

    def who_died(self):
        for player in self.players:
            if not player.is_alive() and player not in self.ejected:
                self.ejected.append(player)
                print("Player " + player.get_name() + " was expelled")
        for monster in self.adversaries:
            if not monster.is_alive() and monster not in self.ejected:
                print("Monster " + monster.get_name() + " was expelled")

    def move_player_via_id(self, id, pos):
        return self.move_character(self.players[id], pos)

    def draw(self):
        self.current_floor.draw()

    def get_current_floor(self):
        return self.current_floor

    def get_current_floor_index(self):
        return self.current_floor_index

    def get_unlocked(self):
        return self.unlocked

    def get_items(self):
        return self.current_floor.get_items()

    def get_players(self):
        return self.players

    def get_exit(self):
        return self.current_floor.get_exit()

    def set_exit(self, pos):
        self.current_floor.set_exit(pos)

    def get_adversaries(self):
        return self.adversaries

    def get_num_levels(self):
        return len(self.dungeon)

    def get_stats(self):
        return self.character_to_keys, self.character_to_exits

    def unlock(self):
        self.unlocked = True


    def update_status(self):
        dead = len(self.ejected)
        escaped = len(self.exited)
        total_players = len(self.players)
        if dead == total_players:
            self.current_status = Status.LOST
        elif escaped + dead == total_players:
            self.current_status = Status.WON
        elif escaped > 0:
            self.current_status = Status.INPROGRESSWON

    def get_status(self):
        self.update_status()
        return self.current_status

    def next_level(self):
        self.current_floor_index += 1
        if self.current_floor_index < len(self.dungeon):
            self.current_floor = self.dungeon[self.current_floor_index]
            self.items = self.current_floor.get_items()
            self.unlocked = self.lock_status()
            self.exited = []
            self.ejected = []
            for player in self.players:
                player.resurrect()
            self.current_status = Status.INPROGRESS
        else:
            raise ValueError("Out of levels")

    def lock_status(self):
        for itemPosn in self.items:
            if itemPosn[0] == "Key" or itemPosn[0] == "key":
                return False
        return True


    def get_intermediate_state(self):
        acc = ""
        acc += "Players: "
        for player in self.players:
            acc += str(player.get_char_position()) + " "
        acc += "\nAdversaries: "
        for adv in self.adversaries:
            acc += str(adv.get_char_position()) + " "
        acc += "\nExit Positions: "
        for level in self.dungeon:
            acc += str(level.get_exit().get_position()) + " "
        return acc

    def get_max_Y_and_X(self):
        return self.current_floor.get_row_and_cols()