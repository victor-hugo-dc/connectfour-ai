from game.connectfour import ConnectFour

class Node:
    def __init__(self, game: ConnectFour, game_copy: ConnectFour = None, parent: 'Node' = None):
        self.game: ConnectFour = game.clone()
        self.game_copy = game_copy
        self.parent: 'Node' = parent
        self.actions = game.get_valid_moves()
        self.children = []
        self.payoff: int = 0
        self.num_paths: int = 0
    
    @property
    def q(self) -> float:
        return self.payoff / (self.num_paths or 1)