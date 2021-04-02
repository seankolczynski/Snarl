import sys

from Common.Observer import Observer


class LocalObserver(Observer):
    def __init__(self):
        self.gameState = None

    def update_gamestate(self, gs):
        self.gameState = gs
        self.gameState.render()

