import sys

from Common.Observer import Observer


class LocalObserver(Observer):
    def __init__(self, id):
        super().__init__(id)
        self.id = id

    def update_state(self, gs, pos):
        self.gameState = gs
        self.position = pos
        if pos is not None:
            self.render(pos)

    def render(self, pos):
        return self.gameState.render()