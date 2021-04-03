import io
import sys
import unittest

import GameState
from Beings import Hero
from Beings.Adversary import Adversary
from Structures import Room, Floor, Hallway


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
        expected = '+---------------------------------------------------------------+\n'\
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X                                                   X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X                           X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                           X X                     X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '+---------------------------------------------------------------+\n'
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
        self.assertEqual(71, floor.rows)
        self.assertEqual(71, floor.cols)
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
        player1 = Hero.Player(2, 1, "Jeff")
        adversary1 = Adversary.Adversary(2, 2, "Zomb", "zombie")
        GameManager.add_adversary(adversary1)
        GameManager.add_player(player1)
        newout = io.StringIO()
        expected = '+---------------------------------------------------------------+\n'\
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X P                             A                   X |\n' \
                   '| X X X X X         e           X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X                           X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                           X X                     X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '+---------------------------------------------------------------+\n'
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
        player1 = Hero.Player(2, 1, "Mike")
        item = "Potion"
        adversary1 = Adversary.Adversary(2, 2, "Bill", "zombie")
        GameManager.add_adversary(adversary1)
        GameManager.add_player(player1)
        GameManager.add_item(item, (5, 6))
        GameManager.move_player_via_id(1, (5, 6))
        newout = io.StringIO()
        expected = '+---------------------------------------------------------------+\n'\
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X                               A                   X |\n' \
                   '| X X X X X P       e           X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X                           X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                           X X                     X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '+---------------------------------------------------------------+\n'
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

    def testItemPickup(self):
        self.maxDiff = None
        example = [[1 for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (20, 5), [])
        zHall = Hallway.Hallway((14, 14), (20, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        floor = Floor.Floor([room, room2], [hall, zHall])
        floor.set_exit((9, 6))
        GameManager = GameState.GameState([floor])
        player1 = Hero.Player(2, 1, "Stan")
        item = "Potion"
        adversary1 = Adversary.Adversary(2, 2, "Jeff", "zombie")
        GameManager.add_adversary(adversary1)
        GameManager.add_player(player1)
        GameManager.add_item(item, (5, 6))
        # Draw initial
        expected = '+---------------------------------------------------------------+\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X P                             A                   X |\n' \
                   '| X X X X X p       e           X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X                           X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                           X X                     X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '+---------------------------------------------------------------+\n' \
                   '+---------------------------------------------------------------+\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '| X X X X X                               A                   X |\n' \
                   '| X X X X X         e P         X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X X X X                     X |\n' \
                   '| X X X X X                     X X                           X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                     X X   X X                     X |\n' \
                   '| X X X X X                           X X                     X |\n' \
                   '| X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X |\n' \
                   '+---------------------------------------------------------------+\n'
        newout = io.StringIO()
        sys.stdout = newout
        floor.draw()
        initial = newout.getvalue()
        #self.assertEqual(expected, initial)
        GameManager.move_player_via_id(1, (5, 6))
        GameManager.move_player_via_id(1, (6, 6))
        GameManager.move_player_via_id(1, (7, 6))
        GameManager.move_player_via_id(1, (8, 6))
        GameManager.move_player_via_id(1, (9, 6))
        GameManager.move_player_via_id(1, (10, 6))
        floor.draw()
        initial = newout.getvalue()
        self.assertEqual(expected, initial)



