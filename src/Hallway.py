"""Describes a layout of tiles connecting two rooms. See examples in LevelTest.py"""
class Hallway:

    def __init__(self, waypoints):
        dots = waypoints
        self.start = waypoints[0]
        self.end = waypoints[len(waypoints) -1]
        self.connectDots = dots