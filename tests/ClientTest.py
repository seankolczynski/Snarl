import io
import sys
import unittest
import json

import Common.JSONToLevel as JLevel
import Client.Client as Cli
from Structures.Tile import WallTile


class MyTestCase(unittest.TestCase):


    def test1(self):
        up = {"type": "player-update", "layout": [[0, 0, 1, 1, 1], [1, 2, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], "position": [9, 11], "objects": [{"type": "key", "position": [10, 10]}], "actors": [{"type": "player", "name": "Sean", "position": [9, 11]}, {"type": "zombie", "name": "1 Zombie", "position": [9, 10]}], "message": ""}

        Cli.player_update(up)


    def test2(self):
        json.loads('{\'type\': \'move\', \'to\': \'"[10,4]"\'}')

    def player_layout(self, grid, position):
        layout = []
        upLeft = ((position[0] - 2), (position[1] - 2))
        downRight = ((position[0] + 2), (position[1] + 2))
        for ind in range((2 * 2) + 1):
            layout.append([])
        for y in range(len(grid[0])):
            count = 0
            for x in range(len(grid)):
                if self.is_in_window(x, y, downRight, upLeft):
                    layout[count].append(grid[x][y].num_val())
                    count = count + 1
        return layout

    def is_in_window(self, x, y, downRight, upLeft):
        return (downRight[0] >= x >= upLeft[0]) and (downRight[1] >= y >= upLeft[1])

    def test3(self):
        example = [[WallTile((i, j)) for i in range(10)] for j in range(10)]
        new = JLevel.player_layout(example, (5, 5))
        old = self.player_layout(example, (5, 5))

