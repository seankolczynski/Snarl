import sys
import unittest

sys.path.append("../src/")

from Player import Player
from Structures.Tile import Tile


class MyTestCase(unittest.TestCase):



    def testRadius(self):
        example = [[Tile((i, j)) for i in range(3)] for j in range(3)]
        example[0][0].add_character(Player(1, 0, "name"))
        adverse = Adversary("Jeff", "zombie", 1, [])
        result = adverse.ring((0,0), (2, 2), example)
        self.assertEqual([(0, 0)], result)
