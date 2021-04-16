import socket
import json
import argparse
import sys

from datetime import datetime, timedelta
sys.path.append("../")
from LocalPlayer.LocalPlayer import LocalPlayer
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager import GameManager
from Enums.CharacterType import CharacterType


class Server():
   
    def __init__(self, ip, port, clients, wait, start_level):

        self.start_level = start_level
        self.ID = 0
        host = ip# Get local machine name
        port = port               
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #
        sock.bind((host, port))
        self.wait = wait
        self.id_to_conn = {}
        # self.id_to_name = {}
        self.server = sock
        self.list_of_players = []
        self.list_of_names = []
        sock.listen(clients)
        self.wait_for_player()
        self.server.settimeout(wait)
        try:
            for _ in range(1, clients):
                self.wait_for_player()
        except socket.timeout:
            print("No additional players")
        if self.ID == 0:
            print("No Players Joined ending Server")
            sock.close()
        start_message = bytes(json.dumps({"type": "start-level", "level": self.start_level, "players": self.list_of_names}), encoding='utf8')
        print(len(self.id_to_conn))
        for conn in self.id_to_conn.values():
            conn.sendall(start_message)

    def wait_for_player(self):
        print("waiting for player")
        conn, addr = self.server.accept()


        print("Got Connection")
        welcome = conn.sendall(bytes(json.dumps({"type": "welcome", "info": "0.1"}), encoding='utf8'))
        while welcome is not None:
            continue
        conn.sendall(bytes("name", encoding='utf8'))
        data2 = conn.recv(1024).decode('utf8')  # buffer size is 1024 bytes
        new_player = LocalPlayer(data2, CharacterType.PLAYER, self.ID)
        # self.id_to_name[self.ID] = str(data2)
        self.list_of_players.append(new_player)
        self.list_of_names.append(data2)
        self.id_to_conn[self.ID] = conn
        self.ID += 1
    
    def read(self, ID):
        current_conn = self.id_to_conn[ID]
        current_conn.sendall(bytes("move", encoding='utf8'))
        data = None
        while data == None:
            data = current_conn.recv(1024)
        return json.loads(str(data))
        
    def write(self,str1):
         for conn in self.id_to_conn.values():
            conn.sendall(bytes(str1, encoding='utf8'))  
    
    def close(self):
        self.server.close()
 
    def start_new_level(self, level_num):
        for conn in self.id_to_conn.values():
            conn.sendall(bytes(json.dumps({"type": "start-level", "level": level_num+1, "players": self.list_of_players }), encoding='utf8'))
      



if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--clients", help="number of players", action="store", type=int, default=4)
    ap.add_argument("--wait", help="seconds to time out", action="store", type=int, default=60)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=0)
    ap.add_argument("--address", help="address to host", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)

    args = ap.parse_args()
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
    if args.start > len(floors) or args.start < 1:
        raise ValueError("invalid floor index")

    start_level_index = args.start - 1
    init_gamestate = GameState(floors)
    init_gamemanager = GameManager(init_gamestate, server, parsed_levels)
    for player in server.list_of_players:
        init_gamemanager.register_player_user(player)
    if args.observe == 1:
        init_gamemanager.register_observer(Observer(-1))
    init_gamemanager.set_starting_level(1)
    init_gamemanager.start_game()
