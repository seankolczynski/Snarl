import io
import sys
import unittest

import Hallway
import Level
import Room


class MyTestCase(unittest.TestCase):
    # Tests that our level draws properly
    def testDefaultRoom(self):
        self.maxDiff = None
        example = [[" " for i in range(10)] for j in range(10)]
        hall = Hallway.Hallway((14, 5), (21, 5), [])
        zHall = Hallway.Hallway((14, 14), (21, 10), [(17, 14), (17, 10)])
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (20, 5))
        level = Level.Level([room, room2], [hall, zHall])
        newout = io.StringIO()
        expected = '┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                                                   X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X X X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X                           X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                     X X   X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X                           X X                     X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n│ X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X X │\n└─────────────────────────────────────────────────────────────────────────────────────────────────────┘\n'
        sys.stdout = newout
        level.draw()
        endVal = newout.getvalue()
        # Because the level exit is randomly placed, we had to remove it from the test
        if endVal.__contains__("e"):
            endVal = endVal.replace("e", " ")
        self.assertEqual(expected, endVal)

    # Tests that levels will not allow invalid layouts
    def testValidation(self):
        example = [[" " for i in range(10)] for j in range(10)]
        room = Room.Room(example, (5, 5))
        room2 = Room.Room(example, (6, 5))
        with self.assertRaises(ValueError):
            Level.Level([room, room2], [])


if __name__ == '__main__':
    unittest.main()
