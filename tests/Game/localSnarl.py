import argparse
import sys
from os import system, name

sys.path.append("../../src/")
# sys.path.append("../../src/Common")
# sys.path.append("../../src/Enums")
# sys.path.append("../../src/Monsters")
# sys.path.append("../../src/Observer")
# sys.path.append("../../src/Player")
# sys.path.append("../../src/Structures")
from LocalPlayer.LocalPlayer import LocalPlayer


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help="path to level spec", action="store", default="snarl.levels")
    ap.add_argument("--players", help="number of players", action="store", type=int, default=1)
    ap.add_argument("--start", help="Level to start from", action="store", type=int, default=1)
    ap.add_argument("--observe", help="Level to start from", action="store", type=int, default=0)

    args = ap.parse_args()
    if args.players != 1:
        raise ValueError("Illegal amount of players given")
    print(args.players)

    uuid = 1
    list_of_players = []
    for i in range(0, args.players):
        char_name = input("enter a name for your character")
        new_player = LocalPlayer(char_name, "player", uuid, [])
        list_of_players.append(new_player)

    path_to_levels = args.levels
    try:
        levels = open(path_to_levels)
        levels_raw = levels.read()
        levels.close()
        parsed_levels = levels_raw.split("\n")
        if len(parsed_levels) == 1 or int(parsed_levels[0]) != len(parsed_levels[1:]):
            raise ValueError("invalid levels file format")


    except ValueError:
        print("Input files level given is not valid")


