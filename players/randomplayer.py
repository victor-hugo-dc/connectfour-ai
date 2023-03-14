import random
from players.baseplayer import BasePlayer
from game.connectfour import ConnectFour

class RandomPlayer(BasePlayer):
    def __init__(self) -> None:
        pass

    def move(self, game: ConnectFour) -> int:
        return random.choice(game.get_valid_moves())