import socket
import json
import argparse
import sys
import time

from datetime import datetime
sys.path.append("../src/")
from LocalPlayer.LocalPlayer import LocalPlayer
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager1 import GameManager1 as GameManager
from Enums.CharacterType import CharacterType
from Remote.ServerMulti import Server



if __name__ == "__main__":
    replay = True
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--clients", help="number of players", action="store", type=int, default=4)
    ap.add_argument("--wait", help="seconds to time out", action="store", type=int, default=60)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=0)
    ap.add_argument("--address", help="address to host", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)

    args = ap.parse_args()
    already = []

    server = None
    while replay:
        # time.sleep()
        server = Server(args.address,args.port,args.clients,args.wait, args.levels)
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
        # if args.start > len(floors) or args.start < 1:
        #     raise ValueError("invalid floor index")

        # start_level_index = args.start - 1
        init_gamestate = GameState(floors)
        # init_gamestate.set_stats(key_dict, exit_dict, eject_dict)
        init_gamemanager = GameManager(init_gamestate, server, parsed_levels)
        for player in server.list_of_players:
            init_gamemanager.register_player_user(player)
        if args.observe == 1:
            init_gamemanager.register_observer(Observer(-1))
        # init_gamemanager.set_starting_level(1)
        init_gamemanager.start_game()
        init_gamemanager.leaderboard_stats(already)
        already = init_gamemanager.get_end_game_stats()
        replay = server.ask_head_for_replay()
        print("REPLAY " + str(replay))
        server.close()