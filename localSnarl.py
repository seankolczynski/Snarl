import argparse
import PlayerUser
if __name__ == "__main__":
    ap = argparse.ArgumentParser()

    ap.add_argument("--levels", help = "path to level spec", action = "store", default = "snarl.levels")
    ap.add_argument("--players", help = "number of players", action = "store", type=int, default = 1)
    ap.add_argument("--start", help = "Level to start from", action = "store", type=int, default = 1)
    ap.add_argument("--observe", help = "Level to start from", action = "store", type=int, default = 0)

    args = ap.parse_args()
    if args.players != 1:
        raise ValueError("Illegal amount of players given")
    print(args.players)
    
    uuid = 1 
    list_of_players = []
    for i in range(0, args.players):
        char_name = input("enter a name for your character")
        new_player = PlayerUser(char_name, "player, uuid, [])
        list_of_players.append(new_player)
    