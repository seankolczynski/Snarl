import json
import unittest
import sys
sys.path.append("../src/")
from Tile import WallTile, Tile
from Room import Room



def roomMaker(room):
    origin = (room["origin"][1], room["origin"][0])
    rows = room["bounds"]["rows"]
    cols = room["bounds"]["columns"]
    layout = room["layout"]
    doors = []
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
    for door in doors:
        final.addDoor(door)

    return final

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
        return json.dumps(["Failure: Point ", point, " in not in room at ", origin])
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
    return json.dumps(["Success: Traversable points from ", point, " in room at ", origin, " are ", points])


class testSuite(unittest.TestCase):

    def test1(self):
        input_string_f = open("./Level/1-in.json")
        input_string =  input_string_f.read()
        expected_f = open("./Level/1-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        room = valid[0]
        point = valid[1]
        finalRoom = roomMaker(room)
        self.assertEqual(expected, roomChecker(finalRoom, point))
        input_string_f.close()
        expected_f.close()

    def test2(self):
        input_string_f = open("./Level/2-in.json")
        input_string =  input_string_f.read()
        expected_f = open("./Level/2-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        room = valid[0]
        point = valid[1]
        finalRoom = roomMaker(room)
        self.assertEqual(expected, roomChecker(finalRoom, point))
        input_string_f.close()
        expected_f.close()

    def test3(self):
        input_string_f = open("./Level/3-in.json")
        input_string =  input_string_f.read()
        expected_f = open("./Level/3-out.json")
        expected = expected_f.read()
        valid = json.loads(input_string)
        room = valid[0]
        point = valid[1]
        finalRoom = roomMaker(room)
        self.assertEqual(expected, roomChecker(finalRoom, point))
        input_string_f.close()
        expected_f.close()
     
if __name__ == "__main__":
    print("Please provide your JSONS. When you are done, hit CTRL-D twice\n")
    input_str = sys.stdin.read()
    if input_str == "-test":
        unittest.main() 
    valid = json.loads(input_str)
    room = valid[0]
    point = valid[1]
    finalRoom = roomMaker(room)
    print(roomChecker(finalRoom, point))





