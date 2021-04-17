import io
import sys
import unittest

import GameState
from Beings import Hero
from Beings.Adversary import Adversary
from Structures import Room, Floor, Hallway
import Client.Client as Cli


class MyTestCase(unittest.TestCase):


    def test1(self):
        up = {"type": "player-update", "layout": [[0, 0, 1, 1, 1], [1, 2, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], "position": [9, 11], "objects": [{"type": "key", "position": [10, 10]}], "actors": [{"type": "player", "name": "Sean", "position": [9, 11]}, {"type": "zombie", "name": "1 Zombie", "position": [9, 10]}], "message": ""}

        Cli.player_update(up)
