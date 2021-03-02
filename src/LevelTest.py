import io
import sys
import unittest
import Hallway, Floor, Room, GameState, Player, Adversary
from Tile import Tile, WallTile


class MyTestCase(unittest.TestCase):
    # Tests that our floor draws properly
    def testDefaultRoom(self):
        self.maxDiff = None
        example = [[Tile(i, j) for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (21, 5), [])
        zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        floor = Floor.Floor([room, room2], [hall, zHall])
        newout = io.StringIO()
        expected = '┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐\n'\
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
        example = [[Tile(i, j) for i in range(10)] for j in range(10)]
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (6, 5))
        with self.assertRaises(ValueError):
            Floor.Floor([room, room2], [])

    # Tests that floors will not allow invalid layouts
    def testExpand(self):
        example = [[Tile(i, j) for i in range(10)] for j in range(10)]
        room = Room.Room(example, (60, 60))
        floor = Floor.Floor([room], [])
        self.assertEqual(70, floor.rows)
        self.assertEqual(70, floor.cols)
        floor.draw()
    
    def testIntermediateOutput(self):
        self.maxDiff = None
        example = [[Tile(i, j) for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (21, 5), [])
        zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        floor = Floor.Floor([room, room2], [hall, zHall])
        newout = io.StringIO()
        GameManger = GameState([Floor])
        player1 = Player(2);
        adversary1 = Adversary(2);
        GameManger.add_adversary(adversary1)
        GameManger.add_adversary(player1)
        self.assertEqual(GameManger.get_intermediate_state(), "") 

    #Checks that a room's doors are updated
    def testDoors(self):
        example = [[Tile(i, j) for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (21, 5), [])
        zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
        #room = Room.Room(exam)ple, (5, 5))
