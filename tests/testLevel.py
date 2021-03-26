#!/usr/bin/env python
import json
import unittest
import sys

sys.path.append("../src/")
from Tile import WallTile, Tile, ExitTile
from Room import Room
from Floor import Floor
from Item import Item
from Hallway import Hallway


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
    key_pos = floor["objects"][0]["position"]
    exit_pos = floor["objects"][1]["position"]
    new_floor = Floor(rooms, hallways)
    new_floor.set_exit(translate_to_xy(exit_pos))
    new_floor.place_item("Key", translate_to_xy(key_pos))
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


def translate_to_xy(rowCol):
    y, x = rowCol
    return (x, y)


class testSuite(unittest.TestCase):

    def test1(self):
        input_string_f = open("Level/1-in.json")
        input_string = input_string_f.read()
        input_string_f.close()
        expected_f = open("Level/1-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        floor = valid[0]
        point = translate_to_xy(valid[1])
        finalFloor = floorMaker(floor)
        self.assertEqual(expected, floorChecker(finalFloor, point))



    def test2(self):
        input_string_f = open("Level/2-in.json")
        input_string = input_string_f.read()
        input_string_f.close()
        expected_f = open("Level/2-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        floor = valid[0]
        point = translate_to_xy(valid[1])
        finalFloor = floorMaker(floor)
        finalFloor.draw()
        self.assertEqual(expected, floorChecker(finalFloor, point))
        input_string_f.close()
        expected_f.close()

    def test3(self):
        input_string_f = open("Level/3-in.json")
        input_string = input_string_f.read()
        input_string_f.close()
        expected_f = open("Level/3-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        floor = valid[0]
        point = translate_to_xy(valid[1])
        finalFloor = floorMaker(floor)
        self.assertEqual(expected, floorChecker(finalFloor, point))
        input_string_f.close()
        expected_f.close()

    def test4(self):
        input_string_f = open("Level/4-in.json")
        input_string = input_string_f.read()
        input_string_f.close()
        expected_f = open("Level/4-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        floor = valid[0]
        point = translate_to_xy(valid[1])
        finalFloor = floorMaker(floor)
        self.assertEqual(expected, floorChecker(finalFloor, point))
        input_string_f.close()
        expected_f.close()



if __name__ == "__main__":
    print("Please input json, then push ctrl-d")
    input_str = sys.stdin.read()
    if input_str == "-test":
        unittest.main()
    valid = json.loads(input_str)
    floor = valid[0]
    point = valid[1]
    finalRoom = floorMaker(floor)
    print(finalRoom.draw())
    #print(roomChecker(finalRoom, point))
