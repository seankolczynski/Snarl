import sys
import unittest
from typing import io

from GameManager import GameManager
from GameState import GameState
from Hallway import Hallway
from Room import Room
from Floor import Floor
from PlayerUser import PlayerUser

class MyTestCase(unittest.TestCase):

    playerUser1 = PlayerUser("player", 0)
    playerUser2 = PlayerUser("player", 1)

    def testRegisterUsers(self):
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway((14, 5), (20, 5), [])
        zHall = Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room(example, (5, 5))
        room2 = Room(example, (20, 5))
        floor = Floor([room, room2], [hall, zHall])
        game = GameState([floor])
        gm = GameManager(game)
        gm.register_player_user(self.playerUser1)
        gm.register_player_user(self.playerUser2)
        self.assertEqual(2, len(gm.ID_to_user))

    # def testUpdateUsers(self):
    #     example = [[1 for i in range(10)] for j in range(10)]
    #     hall = Hallway((14, 5), (20, 5), [])
    #     zHall = Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
    #     room = Room(example, (5, 5))
    #     room2 = Room(example, (20, 5))
    #     floor = Floor([room, room2], [hall, zHall])
    #     game = GameState([floor])
    #     gm = GameManager(game)
    #     gm.register_player_user(self.playerUser1)
    #     gm.register_player_user(self.playerUser2)
    #     gm.requ

