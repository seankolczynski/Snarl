import socket
import json
import argparse
import sys

sys.path.append("../")
from RemotePlayer import RemotePlayer
from RemoteAdversary import RemoteAdversary
import Common.JSONToLevel as JLevel
from Common.Observer import Observer
from GameState import GameState
from GameManager import GameManager
from Enums.CharacterType import CharacterType


class Server():

    def __init__(self, ip, port, clients, wait, start_level):

        self.start_level = start_level
        self.ID = 0
        host = ip  # Get local machine name
        port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
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
        start_message = bytes(
            json.dumps({"type": "start-level", "level": self.start_level, "players": self.list_of_names}) + "\n",
            encoding='utf8')
        print(len(self.id_to_conn))
        for conn in self.id_to_conn.values():
            conn.sendall(start_message)

    def wait_for_player(self):
        print("waiting for player")
        conn, addr = self.server.accept()

        print("Got Connection")
        welcome = conn.sendall(bytes(json.dumps({"type": "welcome", "info": "0.1"}) + "\n", encoding='utf8'))
        while welcome is not None:
            continue
        conn.sendall(bytes("name" + "\n", encoding='utf8'))
        data2 = conn.recv(1024).decode('utf8')  # buffer size is 1024 bytes

        new_player = self.request_type(conn, data2)
        # self.id_to_name[self.ID] = str(data2)

        self.list_of_players.append(new_player)
        self.list_of_names.append(data2)
        self.id_to_conn[self.ID] = conn
        self.ID += 1

    def request_type(self, conn, name):
        conn.sendall(bytes("Hero[1] or Adversary[2]?\n", encoding='utf8'))
        genre = conn.recv(1024).decode('utf8')
        try:
            if '1' in genre:
                conn.sendall(bytes("You have chosen to play as a Hero! A valiant decision.\n", encoding='utf8'))
                return RemotePlayer(name, CharacterType.PLAYER, self.ID, self)
            elif '2' in genre:
                conn.sendall(bytes("Will you be a Zombie[1] or a Ghost[2]?\n", encoding='utf8'))
                title = conn.recv(1024).decode('utf8')
                if '2' in title:
                    conn.sendall(bytes("You have chosen to play as a Ghost Adversary!\n", encoding='utf8'))
                    return RemoteAdversary(name, CharacterType.GHOST, self.ID, self)
                else:
                    conn.sendall(bytes("You have chosen to play as a Zombie Adversary!\n", encoding='utf8'))
                    return RemoteAdversary(name, CharacterType.ZOMBIE, self.ID, self)
            else:
                return self.request_type(conn, name)
        except:
            return self.request_type(conn, name)

    def read(self, ID):
        current_conn = self.id_to_conn[ID]
        current_conn.sendall(bytes("move" + "\n", encoding='utf8'))
        data = None
        while data == None:
            data = current_conn.recv(1024).decode('utf8')
            print(data)
        translated = json.loads(str(data))
        return translated

    def ask_head_for_replay(self):
        current_conn = self.id_to_conn[1]
        current_conn.sendall(bytes(json.dumps({"type": "replay"}) + "\n", encoding='utf8'))
        data = None
        while data == None:
            data = current_conn.recv(1024).decode('utf8')
            print(data)
        translated = str(data)
        return translated

    def write(self, str1):
        for conn in self.id_to_conn.values():
            conn.sendall(bytes(str1 + "\n", encoding='utf8'))

    def write_to_id(self, message, id):
        self.id_to_conn[id].sendall(bytes(message + "\n", encoding="utf8"))

    def close(self):
        self.server.close()

    def start_new_level(self, level_num):
        for conn in self.id_to_conn.values():
            conn.sendall(bytes(
                json.dumps({"type": "start-level", "level": str(level_num + 1), "players": self.list_of_names}) + "\n",
                encoding='utf8'))


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
    key_dict, exit_dict, eject_dict = {}, {}, {}
    server = None
    while replay:
        server = Server(args.address, args.port, args.clients, args.wait, args.levels)
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
        init_gamestate.set_stats(key_dict, exit_dict, eject_dict)
        init_gamemanager = GameManager(init_gamestate, server, parsed_levels)
        for player in server.list_of_players:
            init_gamemanager.register_player_user(player)
        if args.observe == 1:
            init_gamemanager.register_observer(Observer(-1))
        init_gamemanager.set_starting_level(1)
        init_gamemanager.start_game()
        key_dict_1, exit_dict_2, eject_dict_3 = init_gamestate.get_stats()
        replay = server.ask_head_for_replay()
    server.close()

