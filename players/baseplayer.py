from abc import ABC, abstractmethod

class BasePlayer:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def move(self, game, player) -> int:
        pass