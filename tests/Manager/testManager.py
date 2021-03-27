#!/usr/bin/env python
import json
import unittest
import sys

sys.path.append("../../src/")
from Tile import WallTile, Tile, ExitTile
from Room import Room
from Floor import Floor
from Hallway import Hallway
from GameState import GameState
from GameManager import GameManager
from PlayerUser import PlayerUser
from Adversary import Adversary
import random
import pprint



monster_types = ["zombie", "ghost"]
name_list = ["George", "Michael", "Lucille", "Andy", "Tobias"]

def managerMaker(jsonStuff):
    names = jsonStuff[0]
    floor = jsonStuff[1]
    natural = jsonStuff[2]
    ptList = jsonStuff[3]
    actorMoveLL = moves_parser(jsonStuff[4])
    levelMade = floorMaker(floor)
    testState = GameState([levelMade])
    manager = GameManager(testState)
    users = []
    index = 0
    for name in names:
        newUser = PlayerUser(name, "player", index, actorMoveLL[index])
        manager.register_player_user(newUser)
        testState.move_player_via_id(index, translate_to_xy(ptList[index]))
        users.append(newUser)
        index = index + 1
    while index < len(ptList):
        adverse = Adversary(3, index, name_list[index], monster_types[index - 2])
        manager.add_adversary(adverse)
        testState.move_character(adverse, translate_to_xy(ptList[index]))
        index = index + 1
    return (manager, natural, users)

def artificial_game_run(maxi, manager, users, level):
    manager.init_Rule_Checker()
    manager.update_gamestate()
    JSON_response = []
    for user2 in users:
        JSON_response.append([user2.get_name(), player_update_gather(user2)])
    round_number = 0
    manager.game.draw()
    while round_number < maxi:
        turn_index = 0
        for user in users:
            attempted_move = user.get_next_move()
            if attempted_move is None:
                return json.dumps([stateToJSON(manager.game, level), JSON_response])#, indent=4, sort_keys=True)
            results = manager.take_turn(turn_index)
            for result in results:
                if result == "Done":
                    return json.dumps([stateToJSON(manager.game, level), JSON_response])#, indent=4, sort_keys=True)
                simple = reinterpret(result[1])
                JSON_response.append([user.get_name(), {"type": "move", "to": translate_to_xy(result[0])}, simple])
            for user2 in users:
                if user2.position is not None:
                    JSON_response.append([user2.get_name(), player_update_gather(user2)])
            if manager.game.is_over():
                return json.dumps([stateToJSON(manager.game, level), JSON_response])
            turn_index = turn_index + 1
        round_number = round_number + 1
        manager.game.draw()
    manager.game.draw()
    return json.dumps([stateToJSON(manager.game, level), JSON_response])#, indent=4, sort_keys=True)

def reinterpret(message):
    if message == 'Invalid':
        return "Invalid"
    if message['success']:
        info = message['message']
        if "Ejected" in info:
            return "Eject"
        if "Key" in info or "OK" in info:
            return info
        if "Exited" in info:
            return "Exit"



def player_update_gather(user):
    j_type = "player-update"
    layout = user.get_view()
    position = user.get_position()

    breakdown = layout_parser(layout, user.get_name())
    return {"type": j_type, "position": translate_to_xy(position), "layout": breakdown[0],
            "objects": breakdown[1], "actors": breakdown[2]}


def layout_parser(layout, username):
    rows = []
    item_tiles = []
    actor_tiles = []
    for y in range(len(layout)):
        row = []
        for x in range(len(layout)):
            current_tile = layout[x][y]
            row.append(current_tile.num_val())
            items = current_tile.get_all_items()
            if len(items) > 0 or isinstance(current_tile, ExitTile):
                item_tiles.append(current_tile)
            actor = current_tile.get_character()
            if actor is not None and actor.get_name() != username:
                actor_tiles.append(current_tile)

        rows.append(row)
    itemJSON = []
    for tile in item_tiles:
        if isinstance(tile, ExitTile):
            itemJSON.append({"type": "exit", "position": translate_to_xy(tile.get_position())})
        for item in tile.get_all_items():
            itemJSON.append({"type": item.get_name(), "position": translate_to_xy(tile.get_position())})
    actorJSON = []
    for tile in actor_tiles:
        act = tile.get_character()
        actorJSON.append({"type": act.get_ctype(), "name": act.get_name(), "position": translate_to_xy(tile.get_position())})
    return (rows, itemJSON, actorJSON)



def moves_parser(listOfLists):
    moveBook = []
    for moveset in listOfLists:
        moveList = []
        for move in moveset:
            moveList.append(translate_to_xy(move["to"]))
        moveBook.append(moveList)
    return moveBook



def roomMaker(room):
    origin = (room["origin"][1], room["origin"][0])
    rows = room["bounds"]["rows"]
    cols = room["bounds"]["columns"]
    layout = room["layout"]
    grid = []
    for col in range(cols):
        column = []
        for row in range(rows):
            if layout[row][col] == 2:
                column.append(1)
            else:
                column.append(layout[row][col])
        grid.append(column)

    final = Room(grid, origin)
    return final


def hallMaker(hall):
    from_hall = translate_to_xy(hall["from"])
    to_hall = translate_to_xy(hall["to"])
    waypoints = hall["waypoints"]
    fixed_waypoints = []
    for w in waypoints:
        fixed_waypoints.append(translate_to_xy(w))
    new_hallway = Hallway(from_hall, to_hall, fixed_waypoints)
    return new_hallway


def floorMaker(floor):
    rooms = list(map(lambda x: roomMaker(x), floor["rooms"]))
    hallways = list(map(lambda x: hallMaker(x), floor["hallways"]))
    new_floor = Floor(rooms, hallways)
    objects = floor["objects"]
    for objecto in objects:
        if objecto['type'] == 'exit':
            exit_pos = objecto["position"]
            new_floor.set_exit(translate_to_xy(exit_pos))
        elif objecto['type'] == 'key':
            key_pos = objecto["position"]
            new_floor.place_item("key", translate_to_xy(key_pos))
        else:
            new_floor.place_item(objecto["type"], translate_to_xy(objecto["position"]))
    return new_floor


def roomChecker(room, point):
    up = (point[0] - 1, point[1])
    down = (point[0] + 1, point[1])
    right = (point[0], point[1] + 1)
    left = (point[0], point[1] - 1)
    origin = room.get_origin()
    origin_translated = (origin[1], origin[0])
    height = room.height
    width = room.width
    minRow = origin_translated[0]
    maxRow = origin_translated[0] + height - 1
    minCol = origin_translated[1]
    maxCol = origin_translated[1] + width - 1
    points = []

    if point[0] < minRow or point[0] > maxRow or point[1] < minCol or point[1] > maxCol:
        return json.dumps(["Failure: Point ", point, " in not in room at ", origin_translated])
    if minRow <= up[0] <= maxRow and minCol <= up[1] <= maxCol:
        if not isinstance(room.get_tile((up[1], up[0])), WallTile):
            points.append(up)
    if minRow <= left[0] <= maxRow and minCol <= left[1] <= maxCol:
        if not isinstance(room.get_tile((left[1], left[0])), WallTile):
            points.append(left)
    if minRow <= right[0] <= maxRow and minCol <= right[1] <= maxCol:
        if not isinstance(room.get_tile((right[1], right[0])), WallTile):
            points.append(right)
    if minRow <= down[0] <= maxRow and minCol <= down[1] <= maxCol:
        if not isinstance(room.get_tile((down[1], down[0])), WallTile):
            points.append(down)
    return json.dumps(["Success: Traversable points from ", point, " in room at ", origin_translated, " are ", points])


def floorChecker(floor, point):
    specific_tile = floor.get_tile_at(point)
    trav = not isinstance(specific_tile, WallTile)
    item = None
    structure = "void"
    inside = specific_tile.get_room()
    if (isinstance(inside, Room)):
        structure = "room"
    if (isinstance(inside, Hallway)):
        structure = "hallway"
    reachable = []
    if trav:
        if specific_tile.get_item_with_name("Key") != None:
            item = "key"
        if isinstance(specific_tile, ExitTile):
            item = "exit"
        reached = floor.reaches(inside)
        for r in reached:
            corner = r.get_origin()
            reachable.append((corner[1], corner[0]))

    return json.dumps({"traversable": trav, "object": item, "type": structure, "reachable": reachable})


def stateToJSON(game, level):
    typo = "state"
    level = levelToJSON(game, level)
    players = playersToJSON(game)
    adversaries = adversariesToJSON(game)
    exitLocked = not game.get_unlocked()
    return {"type": typo, "level": level, "players": players, "adversaries": adversaries, "exit-locked": exitLocked}


def levelToJSON(game, level):
    objects = game.get_items()
    objectJSONs = []
    exit = game.get_exit()
    objectJSONs.append({"type": "exit", "position": translate_to_xy(exit.get_position())})
    for obj in objects:
        objectJSONs.append({"type": obj[0], "position": translate_to_xy(obj[1])})
    return {"type": level["type"], "rooms": level["rooms"], "hallways": level["hallways"], "objects": objectJSONs}

def playersToJSON(game):
    players = game.get_players()
    playerJSON = []
    for player in players:
        if player.is_alive():
            playerJSON.append({"type": "player", "name": player.get_name(), "position": translate_to_xy(player.get_char_position())})
    return playerJSON

def adversariesToJSON(game):
    adversaries = game.get_adversaries()
    adversaryJSON = []
    for adversary in adversaries:
        adversaryJSON.append({"type": adversary.get_ctype(), "name": adversary.get_name(), "position": translate_to_xy(adversary.get_char_position())})
    return adversaryJSON

def translate_to_xy(rowCol):
    if rowCol == None:
        return rowCol
    y, x = rowCol
    return (x, y)


class testSuite(unittest.TestCase):
    # def test1(self):
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #     self.maxDiff = None
    #     input_string_f = open("1-in.json")
    #     input_string = input_string_f.read()
    #     input_string_f.close()
    #     expected_f = open("1-out.json")
    #     expected = expected_f.read()
    #     expected_f.close()
    #     info = json.loads(input_string)
    #     manager, maxi, users = managerMaker(info)
    #     #print(artificial_game_run(maxi, manager, users, info[1]))
    #     self.assertEqual(expected, artificial_game_run(maxi, manager, users, info[1]))
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # def test2(self):
    #     self.maxDiff = None
    #     input_string_f = open("2-in.json")
    #     input_string = input_string_f.read()
    #     input_string_f.close()
    #     expected_f = open("2-out.json")
    #     expected = expected_f.read()
    #     expected_f.close()
    #     info = json.loads(input_string)
    #     manager, maxi, users = managerMaker(info)
    #     # print(artificial_game_run(maxi, manager, users, info[1]))
    #     self.assertEqual(expected, artificial_game_run(maxi, manager, users, info[1]))
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    # def test3(self):
    #     self.maxDiff = None
    #     input_string_f = open("3-in.json")
    #     input_string = input_string_f.read()
    #     input_string_f.close()
    #     expected_f = open("3-out.json")
    #     expected = expected_f.read()
    #     expected_f.close()
    #     info = json.loads(input_string)
    #     manager, maxi, users = managerMaker(info)
    #     # print(artificial_game_run(maxi, manager, users, info[1]))
    #     self.assertEqual(expected, artificial_game_run(maxi, manager, users, info[1]))
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    def test4(self):
        self.maxDiff = None
        input_string_f = open("4-in.json")
        input_string = input_string_f.read()
        input_string_f.close()
        expected_f = open("4-out.json")
        expected = expected_f.read()
        expected_f.close()
        info = json.loads(input_string)
        manager, maxi, users = managerMaker(info)
        # print(artificial_game_run(maxi, manager, users, info[1]))
        self.assertEqual(expected, artificial_game_run(maxi, manager, users, info[1]))
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    # def test2(self):
    #     input_string_f = open("2-in.json")
    #     input_string = input_string_f.read()
    #     input_string_f.close()
    #     expected_f = open("2-out.json")
    #     expected = expected_f.read()
    #     valid = json.loads(input_string)
    #     floor = valid[0]
    #     point = translate_to_xy(valid[1])
    #     finalFloor = floorMaker(floor)
    #     finalFloor.draw()
    #     self.assertEqual(expected, floorChecker(finalFloor, point))
    #     input_string_f.close()
    #     expected_f.close()

    # def test3(self):
    #     input_string_f = open("../Level/3-in.json")
    #     input_string = input_string_f.read()
    #     input_string_f.close()
    #     expected_f = open("../Level/3-out.json")
    #     expected = expected_f.read()
    #     valid = json.loads(input_string)
    #     floor = valid[0]
    #     point = translate_to_xy(valid[1])
    #     finalFloor = floorMaker(floor)
    #     self.assertEqual(expected, floorChecker(finalFloor, point))
    #     input_string_f.close()
    #     expected_f.close()

    # def test4(self):
    #     input_string_f = open("../Level/4-in.json")
    #     input_string = input_string_f.read()
    #     input_string_f.close()
    #     expected_f = open("../Level/4-out.json")
    #     expected = expected_f.read()
    #     valid = json.loads(input_string)
    #     floor = valid[0]
    #     point = translate_to_xy(valid[1])
    #     finalFloor = floorMaker(floor)
    #     self.assertEqual(expected, floorChecker(finalFloor, point))
    #     input_string_f.close()
    #     expected_f.close()


if __name__ == "__main__":
    # print("Please input json, then push ctrl-d")
    # input_str = sys.stdin.read()
    # if input_str == "-test":
        unittest.main()
    # valid = json.loads(input_str)
    # floor = valid[0]
    # point = valid[1]
    # finalRoom = floorMaker(floor)
    # print(finalRoom.draw())
    # print(roomChecker(finalRoom, point))
