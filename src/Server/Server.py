import socket
import json
import argparse
import sys

from datetime import datetime
sys.path.append("../")
from LocalPlayer.LocalPlayer import LocalPlayer
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager import GameManager
from Enums.CharacterType import CharacterType


class Server():
   
    def __init__(self,ip, port, clients, wait, start_level):

        self.start_level = start_level
        self.ID = 0
        host = ip# Get local machine name
        port = port               
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #
        sock.bind((host, port))
        time_change = datetime.timedelta(seconds=wait)
        end_time = datetime.datetime.now() + time_change
        self.id_to_conn = {}
        # self.id_to_name = {}
        self.server = sock
        self.list_of_players = []
        self.list_of_names = []
        sock.listen()
        while datetime.datetime.now() < end_time or self.ID >= clients:
                conn, addr = sock.accept()
                with conn:
                    self.ID += 1 
                    self.id_to_conn[self.ID] = conn 
                    print("Got Connection")
                    conn.sendall(bytes({"type": "welecome", "info": "0.1"}))
                    conn.sendall(bytes("name"))
                    data2 = None
                    while data2 == None:
                        if datetime.datetime.now() < end_time:
                            print("No Players Joined ending Server")
                            sock.close()
                            raise ValueError("player registration timed out") 
                        data2 = conn.recv(1024) # buffer size is 1024 bytes
                    new_player = LocalPlayer(str(data2), CharacterType.PLAYER, self.ID)
                    # self.id_to_name[self.ID] = str(data2)
                    self.list_of_players.append(new_player)
                    self.list_of_names.append(str(data2))
                    end_time = datetime.datetime.now() + time_change 
        if self.ID == 0:
            print("No Players Joined ending Server")
            sock.close()
        for conn in self.id_to_conn.values():
            conn.sendall(bytes({"type": "start-level", "level": self.start_level, "players": self.list_of_players })) 
    
    def read(self, ID):
        current_conn = self.id_to_conn[ID]
        current_conn.sendall(bytes("move"))
        data = None
        while data == None:
            data = current_conn.recv(1024)
        return json.loads(str(data))
        
    def write(self,str1):
         for conn in self.id_to_conn.values():
            conn.sendall(bytes(str1))  
    
    def close(self):
        self.server.close()
 
    def start_new_level(self, level_num)
        for conn in self.id_to_conn.values():
            conn.sendall(bytes({"type": "start-level", "level": level_num+1, "players": self.list_of_players })) 
      



if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--clients", help="number of players", action="store", type=int, default=4)
    ap.add_argument("--wait", help="seconds to time out", action="store", type=int, default=60)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=0)
    ap.add_argument("--address", help="address to host", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)

    args = ap.parse_args()
    server = Server(args.ip,args.port,args.clients,args.wait, args.levels)
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