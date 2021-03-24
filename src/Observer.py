class Observer:
    def __init__(self):
        self.gameState = None


    def update_gamestate(self, gs, pos):
        self.gameState = gs
        self.render(pos)

    def render(self, pos):
        self.gameState.render_in_range(pos, 2)