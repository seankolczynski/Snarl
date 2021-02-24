import json
import re
import sys
sys.path.append("../src/")
from Tile import WallTile, Tile
from Room import Room
import fileinput


def roomMaker(room):
    origin = (room["origin"][1], room["origin"][0])
    rows = room["bounds"]["rows"]
    cols = room["bounds"]["columns"]
    layout = room["layout"]
    doors = []
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            print("Col: " + str(col) + " Rows: " + str(row))
            if layout[row][col] == 0:
                grid[row].append(WallTile((col, row)))
            elif layout[row][col] == 2:
                tile = Tile((col, row))
                doors.append(tile)
                grid[row].append(tile)
            else:
                tile = Tile((col, row))
                grid[row].append(tile)

    final = Room(layout, origin)
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
    maxRow = origin_translated[0] + width - 1
    minCol = origin_translated[1]
    maxCol = origin_translated[1] + height - 1
    points = []

    if point[0] < minRow or point[0] > maxRow or point[1] < minCol or point[1] > maxCol:
        return json.dumps(["Failure: Point ", point, " in not in room at ", origin])
    if minRow <= up[0] <= maxRow and minCol <= up[1] <= maxCol:
        if not isinstance(room.get_tile(up), WallTile):
            points.append(up)
    if minRow <= left[0] <= maxRow and minCol <= left[1] <= maxCol:
        if not isinstance(room.get_tile(left), WallTile):
            points.append(left)
    if minRow <= right[0] <= maxRow and minCol <= right[1] <= maxCol:
        if not isinstance(room.get_tile(right), WallTile):
            points.append(right)
    if minRow <= down[0] <= maxRow and minCol <= down[1] <= maxCol:
        if not isinstance(room.get_tile(down), WallTile):
            points.append(down)
    return json.dumps(["Success: Traversable points from ", point, " in room at ", origin, " are ", points])


if __name__ == "__main__":
    print("Please provide your JSONS. When you are done, hit CTRL-D twice")
    sys.stdin = open("./Level/3-in.json")
    input_str = sys.stdin.read()
    valid = json.loads(input_str)
    room = valid[0]
    point = valid[1]
    finalRoom = roomMaker(room)
    print(roomChecker(finalRoom, point))



