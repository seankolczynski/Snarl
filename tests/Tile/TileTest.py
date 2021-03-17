import io
import sys
import os

from Tile import Tile, WallTile, ExitTile

sys.path.append("../src/")
import unittest
import Hallway, Floor, Room, GameState, Player, Adversary, Item


class MyTestCase(unittest.TestCase):

    def testTile(self):
        tile = Tile((1, 1))
        self.assertEqual((1, 1), tile.get_position())