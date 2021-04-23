import socket
import json
import argparse
import sys

from datetime import datetime
sys.path.append("../src/")
from LocalPlayer.LocalPlayer import LocalPlayer
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager import GameManager
from Enums.CharacterType import CharacterType
from Remote.Server import Server
from Remote.ServerRemoteAd import ServerRemoteAd
from RemotePlayer import RemotePlayer
from RemoteAdversary import RemoteAdversary



if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--clients", help="number of players", action="store", type=int, default=4)
    ap.add_argument("--wait", help="seconds to time out", action="store", type=int, default=4)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=1)
    ap.add_argument("--address", help="address to host", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)

    args = ap.parse_args()
    server = ServerRemoteAd(args.address,args.port,args.clients,args.wait, args.levels)
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

    #start_level_index = 0
    init_gamestate = GameState(floors)
    init_gamemanager = GameManager(init_gamestate, server, parsed_levels)
    identifier = 0
    for name, ctype, conn in server.joined_heros:
        init_gamemanager.register_player_user(RemotePlayer(name, ctype, identifier, server))
        server.id_to_conn[identifier] = conn
        identifier += 1
    for name, ctype, conn in server.joined_advers:
        init_gamemanager.register_player_user(RemoteAdversary(name, ctype, identifier, server))
        server.id_to_conn[identifier] = conn
        identifier += 1
    if args.observe == 1:
        init_gamemanager.register_observer(Observer(-1))
    #init_gamemanager.set_starting_level(1)
    init_gamemanager.start_game()