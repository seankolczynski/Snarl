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