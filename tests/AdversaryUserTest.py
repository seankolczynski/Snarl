import sys
import unittest

sys.path.append("../src/")

from Beings.Hero import Player
from Structures.Room import Room
from Structures.Hallway import Hallway
from Structures.Tile import Tile, WallTile
from AdversaryDriver import AdversaryDriver
from SimpleState import SimpleState


class MyTestCase(unittest.TestCase):

    def testRadiusZombie(self):
        example = [[Tile((i, j)) for i in range(3)] for j in range(3)]
        example[0][0].add_character(Player(1, 0, "name"))
        adverse = AdversaryDriver("Jeff", "zombie", 1, [])
        adverse.gameState = example
        result = adverse.ring((0, 0), (2, 2))
        self.assertEqual([(0, 0)], result)

    def testRadiusGhost(self):
        example = []
        for x in range(3):
            column = []
            for y in range(3):
                if x == 0:
                    column.append(WallTile((x, y)))
                else:
                    column.append(Tile((x, y)))
            example.append(column)
        gost = AdversaryDriver("Boo", "ghost", 2, [])
        gost.gameState = example
        result = gost.ring((0, 0), (2, 2))
        self.assertEqual([(0,0), (0, 2), (0, 1)], result)
        example[2][2].add_character(Player(1, 0, "name"))
        result = gost.ring((0, 0), (2, 2))
        self.assertEqual([(0, 0), (2, 2), (0, 2), (0, 1)], result)

    def testRadiusGhost2(self):
        example = []
        for x in range(5):
            column = []
            for y in range(5):
                if x == 0:
                    column.append(WallTile((x, y)))
                else:
                    column.append(Tile((x, y)))
            example.append(column)
        gost = AdversaryDriver("Boo", "ghost", 2, [])
        gost.gameState = example
        result = gost.ring((0, 0), (4, 4))
        self.assertEqual([(0, 0), (0, 4), (0, 3), (0, 2), (0, 1)], result)
        example[1][1].add_character(Player(1, 0, "name"))
        result = gost.ring((0, 0), (4, 4))
        self.assertEqual([(0, 0), (0, 4), (0, 3), (0, 2), (0, 1)], result)

    def testGhostPickMoves1(self):
        example = []
        for x in range(5):
            column = []
            for y in range(5):
                if x == 0:
                    column.append(WallTile((x, y)))
                else:
                    column.append(Tile((x, y)))
            example.append(column)
        gost = AdversaryDriver("Boo", "ghost", 2, [])
        gost.update_state(SimpleState(example), (2, 2))
        moves = gost.pick_moves()
        self.assertEqual([(2, 1), (1, 2)], moves)

    def testZombiePickMoves1(self):
        room = Room([[]], (0, 0))
        example = []
        for x in range(5):
            column = []
            for y in range(5):
                if x == 0:

                    column.append(WallTile((x, y)))
                else:
                    t = Tile((x, y))
                    t.room = room
                    column.append(Tile((x, y)))
            example.append(column)
        example[1][1].add_character(Player(1, 0, "reggie"))
        gost = AdversaryDriver("Boo", "zombie", 2, [])
        gost.update_state(SimpleState(example), (2, 2))
        moves = gost.pick_moves()
        self.assertEqual([(2, 1)], moves)

    def testGhostPickMoves2(self):
        example = []
        for x in range(5):
            column = []
            for y in range(5):
                if x == 0:
                    column.append(WallTile((x, y)))
                else:
                    column.append(Tile((x, y)))
            example.append(column)
        example[4][2].add_character(Player(1, 0, "reggie"))
        gost = AdversaryDriver("Boo", "ghost", 2, [])
        gost.update_state(SimpleState(example), (2, 2))
        moves = gost.pick_moves()
        self.assertEqual([(3, 2), (2, 1), (1, 2)], moves)

    def testZombieRequestMove1(self):
        room = Room([[]], (0, 0))
        example = []
        for x in range(5):
            column = []
            for y in range(5):
                if x == 0:
                    column.append(WallTile((x, y)))
                else:
                    t = Tile((x, y))
                    t.room = room
                    column.append(Tile((x, y)))
            example.append(column)
        # example[1][1].add_character(Player(1, 0, "reggie"))
        gost = AdversaryDriver("Boo", "zombie", 2, [])
        gost.update_state(SimpleState(example), (2, 2))
        moves = []
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        expected = [(3, 2), (2, 1), (2, 3), (1, 2), (2, 2)]
        for ex in expected:
            self.assertTrue(ex in moves)
        room.addDoor(example[2][1], Hallway((0, 0), (2, 1), []))
        example[2][1].set_room(room)
        moves = []
        state = SimpleState(example)
        gost.update_state(state, (2, 3))
        state.get_tile_at((2, 1)).set_room(room)
        gost.update_state(state, (2, 2))
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        moves.append(gost.request_move())
        expected = [(3, 2), (2, 3), (1, 2), (2, 2)]
        for ex in expected:
            self.assertTrue(ex in moves)






