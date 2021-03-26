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

    playerUser1 = PlayerUser("Bob", "player", 0, [(5, 6)])
    playerUser2 = PlayerUser("Rob", "player", 1, [(7, 7)])

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

    def testUpdateUsers(self):
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
        gm.add_Rule_Checker()
        gm.take_turn(0)
        p1State = self.playerUser1.gameState.grid
        p2State = self.playerUser2.gameState.grid
        p1pos = self.playerUser1.get_position()
        p2pos = self.playerUser2.get_position()
        self.assertEqual(p1State, p2State)
        self.assertEqual((5, 6), p1pos)
        self.assertEqual((6, 5), p2pos)

