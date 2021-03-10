import io
import sys
import os
sys.path.append("../src/")
import unittest
import Hallway, Floor, Room, GameState, Player, Adversary, Item


class MyTestCase(unittest.TestCase):
    # Tests that our floor draws properly
    def testDefaultRoom(self):
        self.maxDiff = None
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (20, 5), [])
        zHall = Hallway.Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        floor = Floor.Floor([room, room2], [hall, zHall])
        newout = io.StringIO()
        expected = '\n┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐\n'\
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                                                   X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X                           X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                           X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '└─────────────────────────────────────────────────────────────────────────────────────────────────────┘\n'
        sys.stdout = newout
        floor.draw()
        endVal = newout.getvalue()
        # Because the floor exit is randomly placed, we had to remove it from the test
        if endVal.__contains__("e"):
            endVal = endVal.replace("e", " ")
        self.assertEqual(expected, endVal)

    # Tests that floors will not allow invalid layouts
    def testValidation(self):
        example = [[1 for i in range(10)] for j in range(10)]
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (6, 5))
        with self.assertRaises(ValueError):
            Floor.Floor([room, room2], [])

    # Tests that floors will not allow invalid layouts
    def testExpand(self):
        example = [[1 for i in range(10)] for j in range(10)]
        room = Room.Room(example, (60, 60))
        floor = Floor.Floor([room], [])
        self.assertEqual(70, floor.rows)
        self.assertEqual(70, floor.cols)
        floor.draw()
    
    def testIntermediateOutput(self):
        self.maxDiff = None
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (20, 5), [])
        zHall = Hallway.Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        floor = Floor.Floor([room, room2], [hall, zHall])
        floor.set_exit((9, 6))
        GameManager = GameState.GameState([floor])
        player1 = Player.Player(2, 1)
        adversary1 = Adversary.Adversary(2, "zombie")
        GameManager.add_adversary(adversary1)
        GameManager.add_player(player1)
        newout = io.StringIO()
        expected = '\n┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X P                             A                   X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X         e           X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X                           X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                           X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '└─────────────────────────────────────────────────────────────────────────────────────────────────────┘\n'
        sys.stdout = newout
        floor.draw()
        endVal = newout.getvalue()
        self.assertEqual(expected, endVal)

    def testPostMove(self):
        self.maxDiff = None
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (20, 5), [])
        zHall = Hallway.Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        floor = Floor.Floor([room, room2], [hall, zHall])
        floor.set_exit((9, 6))
        GameManager = GameState.GameState([floor])
        player1 = Player.Player(2, 1)
        item = "Potion"
        adversary1 = Adversary.Adversary(2, "zombie")
        GameManager.add_adversary(adversary1)
        GameManager.add_player(player1)
        GameManager.add_item(item, (5, 6))
        GameManager.move_player(1, (5, 6))
        newout = io.StringIO()
        expected = '\n┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                               A                   X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X P       e           X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X                           X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X                           X X                     X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n' \
                   '└─────────────────────────────────────────────────────────────────────────────────────────────────────┘\n'
        sys.stdout = newout
        floor.draw()
        endVal = newout.getvalue()
        self.assertEqual(expected, endVal)

    #Checks that a room's doors are updated
    def testDoors(self):
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (21, 5), [])
        zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
        #room = Room.Room(exam)ple, (5, 5))
