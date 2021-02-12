class Hallway:
    connectDots = []

    def __init__(self, start, end, waypoints):
        self.connectDots.append(start)
        if waypoints:
            for way in waypoints:
                self.connectDots.append(way)
        self.connectDots.append(end)