import socket
import json
import argparse

from datetime import datetime
sys.path.append("../src/")
from LocalPlayer.LocalPlayer import LocalPlayer
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager import GameManager
from Enums.CharacterType import CharacterType


class Server():
   
    def __init__(self,ip, port, clients, wait):

        self.ID = 0
        host = ip# Get local machine name
        port = port               
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #
        sock.bind((host, port))
        time_change = datetime.timedelta(seconds=wait)
        end_time = datetime.datetime.now() + time_change
        self.addr_to_id = {}
        self.server = sock
        self.list_of_players = []
        while datetime.datetime.now() < end_time or self.ID >= clients:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                self.ID += 1 
                self.addr_to_id[addr] = self.ID
                print("Got Connection")
                self.server.sendto(addr, bytes("enter a name for your character: ", "UTF-8"))
                addr2 = None
                data2 = None
                while addr != addr2:
                    data2, addr2 = sock.recvfrom(1024) # buffer size is 1024 bytes
                new_player = LocalPlayer(str(data2), CharacterType.PLAYER, self.ID)
                self.list_of_players.append(new_player)
                end_time = datetime.datetime.now() + time_change 
        if self.ID == 0:
            print("No Players Joined ending Server")
            sock.close()

    def read(self):
       data, addr = self.server.recvfrom(1024)
       return data
    
    def write(self,str1):
        message = bytes(str1, "UTF-8")
        for key in self.addr_to_id.keys():
            self.server.sendto(key,message)



if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--clients", help="number of players", action="store", type=int, default=4)
    ap.add_argument("--wait", help="seconds to time out", action="store", type=int, default=60)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=0)
    ap.add_argument("--address", help="address to host", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)

    args = ap.parse_args()
    server = Server(args.ip,args.port,args.clients,args.wait)
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
    for player in server.list_of_players:
        init_gamemanager.register_player_user(player)
    if args.observe == 1:
        init_gamemanager.register_observer(Observer(-1))
    init_gamemanager.set_starting_level(1)
    init_gamemanager.start_game()
