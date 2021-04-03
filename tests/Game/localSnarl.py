import argparse
import sys
from os import system, name
import json
import math

sys.path.append("../../src/")
from LocalPlayer.LocalPlayer import LocalPlayer
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager import GameManager
from Enums.CharacterType import CharacterType

# def clear():
#     # for windows
#     if name == 'nt':
#         _ = system('cls')

#     # for mac and linux(here, os.name is 'posix')
#     else:
#         _ = system('clear')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--players", help="number of players", action="store", type=int, default=1)
    ap.add_argument("--start", help="Level to start from", action="store", type=int, default=1)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=1)

    args = ap.parse_args()
    # if args.players != 1:
    #     raise ValueError("Illegal amount of players given")
    # print(args.players)

    list_of_players = []
    for id in range(0, args.players):
        char_name = input("enter a name for your character: ")
        new_player = LocalPlayer(char_name, CharacterType.PLAYER, id)
        list_of_players.append(new_player)

    path_to_levels = args.levels

    levels = open(path_to_levels)
    levels_raw = levels.read()
    levels.close()
    parsed_levels = levels_raw.split("\n")
    print(len(parsed_levels))
    floors = []
    if len(parsed_levels) == 1 or int(parsed_levels[0]) != len(parsed_levels[1:]):
        raise ValueError("invalid levels file format")
    for i in range(1, len(parsed_levels)):
        level = parsed_levels[i]
        floors.append(JLevel.floorMaker(json.loads(level)))
    if args.start > len(floors) or args.start < 1:
        raise ValueError("invalid floor index")

    start_level_index = args.start - 1
    init_gamestate = GameState(floors)
    init_gamemanager = GameManager(init_gamestate)
    for player in list_of_players:
        init_gamemanager.register_player_user(player)
    if args.observe == 1:
        init_gamemanager.register_observer(Observer(-1))
    init_gamemanager.set_starting_level(start_level_index)
    init_gamemanager.start_game()



