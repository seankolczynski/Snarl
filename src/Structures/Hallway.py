from Structures.Tile import Tile

"""Describes a layout of tiles connecting two rooms. See examples in LevelTest.py"""
class Hallway:

    def __init__(self, start, end, waypoints):
        dots = []
        dots.append(start)
        if waypoints:
            for way in waypoints:
                dots.append(way)
        dots.append(end)
        self.connectDots = dots

    def get_waypoints(self):
        return self.connectDots

    def generate_tiles(self):
        tiles = []
        length = len(self.connectDots)
        beginning = self.connectDots[0]
        end = self.connectDots[len(self.connectDots) - 1]
        point = 0
        first = beginning
        dotCount = 0
        for dot in self.connectDots:
            if dotCount == 0 or dotCount == len(self.connectDots) - 1:
                dotCount = dotCount + 1
                continue
            til = Tile((dot[0], dot[1]))
            til.set_room(self)
            tiles.append(til)
            dotCount = dotCount + 1
        while point < length - 2:
            nextWay = self.connectDots[point + 1]
            point = point + 1
            startX = first[0]
            startY = first[1]
            nextX = nextWay[0]
            nextY = nextWay[1]
            if startY == nextY:
                lil = min(startX, nextX)
                big = max(startX, nextX)
                cursor = lil + 1
                while cursor < big:
                    hallTile = Tile((cursor, startY))
                    hallTile.set_room(self)
                    tiles.append(hallTile)
                    cursor = cursor + 1
            if startX == nextX:
                lil = min(startY, nextY)
                big = max(startY, nextY)
                cursor = lil + 1
                while cursor < big:
                    hallTile = Tile((startX, cursor))
                    hallTile.set_room(self)
                    tiles.append(hallTile)
                    cursor = cursor + 1
            first = nextWay
        nextWay = self.connectDots[len(self.connectDots) - 1]
        startX = first[0]
        startY = first[1]
        nextX = nextWay[0]
        nextY = nextWay[1]
        if startY == nextY:
            lil = min(startX, nextX)
            big = max(startX, nextX)
            cursor = lil + 1
            while cursor < big:
                hallTile = Tile((cursor, startY))
                hallTile.set_room(self)
                tiles.append(hallTile)
                cursor = cursor + 1
        if startX == nextX:
            lil = min(startY, nextY)
            big = max(startY, nextY)
            cursor = lil + 1
            while cursor < big:
                hallTile = Tile((startX, cursor))
                hallTile.set_room(self)
                tiles.append(hallTile)
                cursor = cursor + 1
        return (beginning, end, tiles)

    def return_neighbors(self):
        neighbors = []
        startRoom = self.start.get_room()
        endRoom = self.end.get_room()
        neighbors.append(startRoom)
        neighbors.append(endRoom)
        return neighbors

    def otherside(self, room):
        neigh = self.return_neighbors()
        if neigh[0] == room:
            return neigh[1]
        else:
            return neigh[0]

    def add_start(self, tile):
        self.start = tile

    def add_end(self, tile):
        self.end = tile

    def door_at(self, pos):
        return pos == self.connectDots[0] or pos == self.connectDots[len(self.connectDots) - 1]