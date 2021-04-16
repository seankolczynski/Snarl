import argparse
import socket
import json


def swap(position):
    return position[1], position[0]

def player_update(update):
    layout = update['layout']
    position = update['position']
    objects = update['objects']
    objectPositions = {}
    for obj in objects:
        objectPositions[(swap(obj['position']))] = obj['type']
    actors = update['actors']
    actorPositions = {}
    for actor in actors:
        actorPositions[(swap(actor['position']))] = actor['type']
    message = update['message']
    image = ""
    image += "+"
    for x in range(5):
        image += "--"
    image += "-+\n"
    for y in range(5):
        image += "| "
        count = 0
        for x in range(5):
            if (x, y) in actorPositions.keys():
                actType = actorPositions[(x, y)]
                if actType == "Zombie" or actType == "zombie":
                    image += "Z"
                elif actType == "Ghost" or actType == "ghost":
                    image += "G"
                elif actType == "Player" or actType == "player":
                    image += "P"
                else:
                    image += "?"
            elif (x, y) in objectPositions.keys():
                objType = objectPositions[(x, y)]
                image += objType[0]
            else:
                if layout[x][y] == 0:
                    image += "X"
                else:
                    image += " "
            image += " "
        image += "|\n"
    image += "+"
    for x in range(5):
        image += "--"
    image += "-+"
    print(image)




if __name__ == "__main__":
    ap = argparse.ArgumentParser()


    ap.add_argument("--address", help="address to connect to", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)
    args = ap.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.address, args.port))
        while True:
            data = s.recv(1024)
            print(data)
            if data == None:
                break
            if str(data) == "name":
                name = input("enter name: ")
                s.sendall(bytes(name))
            elif str(data) == "move":
                move = input("enter a move: ")
                move_json = None
                while move_json == None:
                    try:
                        if move == "":
                            move_json = None
                        else:
                            move_split = move.split(" ")
                            move_json = json.loads("[" + move_split[0] + "," + move_split[1] + "]")
                        s.sendall(json.dumps( {"type": "move", "to": move_json}))
                    except:
                        continue
            elif str(data) == "OK" or str(data) == "Key" or str(data) == "Exit" or str(data) == "Eject" or str(data) == "Invalid":
                print(str(data))
            else:
                server_json = json.loads(data)
                if server_json["type"] == "start-level":
                    print("Starting level #" + server_json["level"] + " with players:")
                    for name in server_json["players"]:
                        print(name)
                elif server_json["type"] == "end-level": 
                    print("Level ended")
                    print("Key was picked up by " + server_json["key"])
                    print("Players who exited:")
                    for name in server_json["exits"]:
                       print(name)
                    print("Players who ejected:")
                    for name in server_json["exits"]:
                       print(name)
                elif server_json["type"] == "end-game":
                    print("End Game Stats:")
                    for score in server_json["scores"]:
                      print(score["name"] + " got " + score["keys"] + " keys, exited " 
                      + score["exits"] + " times, and got ejected " + score["ejected" + " times."] )
                elif server_json["type"] == "player-update":
                    player_update(server_json)
                
                else:
                    print("unknown message recieved closing socket")
                    s.close()
                    break
