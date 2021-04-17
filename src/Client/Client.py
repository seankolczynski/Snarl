import argparse
import socket
import json


def swap(position):
    return position[1], position[0]

def player_update(update):
    layout = update['layout']
    print(layout)
    position = swap(update['position'])
    objects = update['objects']
    objectPositions = {}
    for obj in objects:
        objectPositions[(swap(obj['position']))] = obj['type']
    actors = update['actors']
    actorPositions = {}
    for actor in actors:
        actorPositions[(swap(actor['position']))] = actor['type']
    message = update['message']
    print(position)

    upLeft = ((position[0] - 2), (position[1] - 2))

    image = ""
    image += "+"
    for x in range(5):
        image += "--"
    image += "-+\n"
    for y in range(5):
        image += "| "
        count = 0
        for x in range(5):
            if (x + upLeft[0], y + upLeft[1]) in actorPositions.keys():
                print("X: ", x + upLeft[0], " Y: ", y + upLeft[1])
                actType = actorPositions[(x + upLeft[0], y + upLeft[1])]
                if actType == "Zombie" or actType == "zombie":
                    image += "Z"
                elif actType == "Ghost" or actType == "ghost":
                    image += "G"
                elif actType == "Player" or actType == "player":
                    image += "P"
                else:
                    image += "?"
            elif (x + upLeft[0], y + upLeft[1]) in objectPositions.keys():
                print("X: ", x + upLeft[0], " Y: ", y + upLeft[1])
                objType = objectPositions[(x + upLeft[0], y + upLeft[1])]
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
    print("Current position (format x/yl): ", position)





if __name__ == "__main__":
    ap = argparse.ArgumentParser()


    ap.add_argument("--address", help="address to connect to", action="store", type=str, default="127.0.0.1")
    ap.add_argument("--port", help="port to listen to", action="store", type=int, default=45678)
    args = ap.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.address, args.port))
        welcome = s.recv(34).decode('utf8')
        print(welcome)
        done = False
        while True or not done:
            data_raw = s.recv(1024).decode('utf8')
            data_list = data_raw.split("\n")
            #if data is not None or data != "":
                #print(data)
            for data in data_list:
                if done == True:
                    continue
                print(data)
                if data is None or data == "":
                    pass
                elif data == "name":
                    name = input("enter name: ")
                    s.sendall(bytes(name, encoding='utf8'))
                elif data == "move":
                    move = input("enter a move: ")
                    move_json = None

                    try:
                        if move == "":
                            move_json = None
                        else:
                            move_split = move.split(" ")
                            move_json = json.loads("[" + move_split[0] + "," + move_split[1] + "]")
                        s.sendall(bytes(str({"type": "move", "to": move_json}), encoding='utf8'))
                        print("sent")
                    except:
                        continue
                elif data == "OK" or data == "Key" or data == "Exit" or data == "Eject" or data == "Invalid":
                    print(data)
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
                          print(score["name"] + " got " + str(score["keys"]) + " keys, exited "
                          + str(score["exits"]) + " times, and got ejected " + str(score["ejected"]) + " times." )
                          s.close()
                          done = True
                          break
                    elif server_json["type"] == "player-update":
                        player_update(server_json)
                    elif server_json["type"] == "welcome":
                        break
                    else:
                        print("unknown message received closing socket")
                        done = True
                        s.close()
                        break
