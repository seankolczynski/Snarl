from abc import ABC


class Observer(ABC):

    def __init__(self, id):
        self.id = id

    def update_state(self, gs, pos):
        self.gameState = gs
        self.position = pos
        if pos is not None:
            self.render(pos)

    def render(self, pos):
        print("Observer View")
        return self.gameState.render()


