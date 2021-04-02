import sys
import unittest

sys.path.append("../src/")

from GameManager import GameManager
from GameState import GameState
from Structures.Hallway import Hallway
from Structures.Room import Room
from Structures.Floor import Floor
from LocalPlayer.LocalPlayer import LocalPlayer

class MyTestCase(unittest.TestCase):

    LocalPlayer1 = LocalPlayer("Bob", "player", 0, [(5, 6)])
    LocalPlayer2 = LocalPlayer("Rob", "player", 1, [(7, 7)])

    def testRegisterUsers(self):
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway((14, 5), (20, 5), [])
        zHall = Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room(example, (5, 5))
        room2 = Room(example, (20, 5))
        floor = Floor([room, room2], [hall, zHall])
        game = GameState([floor])
        gm = GameManager(game)
        gm.register_player_user(self.LocalPlayer1)
        gm.register_player_user(self.LocalPlayer2)
        self.assertEqual(2, len(gm.ID_to_user_character))

    def testUpdateUsers(self):
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway((14, 5), (20, 5), [])
        zHall = Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room(example, (5, 5))
        room2 = Room(example, (20, 5))
        floor = Floor([room, room2], [hall, zHall])
        game = GameState([floor])
        gm = GameManager(game)
        gm.register_player_user(self.LocalPlayer1)
        gm.register_player_user(self.LocalPlayer2)
        gm.init_Rule_Checker()
        gm.take_turn(0)
        p1State = self.LocalPlayer1.gameState.grid
        p2State = self.LocalPlayer2.gameState.grid
        p1pos = self.LocalPlayer1.get_position()
        p2pos = self.LocalPlayer2.get_position()
        self.assertEqual(p1State, p2State)
        self.assertEqual((5, 6), p1pos)
        self.assertEqual((6, 5), p2pos)


