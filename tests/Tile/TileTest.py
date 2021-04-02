import sys

from Tile import Tile, WallTile, ExitTile

sys.path.append("../src/")
import unittest


class MyTestCase(unittest.TestCase):

    def testTile(self):
        tile = Tile((1, 1))
        self.assertEqual((1, 1), tile.get_position())
        tile.add_item("Potion")

    def testWallTile(self):
        tile = WallTile((1, 1))
        self.assertEqual((1, 1), tile.get_position())
        with self.assertRaises(TypeError):
            tile.add_item("footprint")


    def testExitTile(self):
        tile = ExitTile((1, 1))
        self.assertEqual((1, 1), tile.get_position())
        tile.add_item("Wand")