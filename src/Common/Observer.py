from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def render(self, pos):
        pass