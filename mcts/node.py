from game.connectfour import ConnectFour

class Node:
    def __init__(self, game: ConnectFour, action: int = None, parent: 'Node' = None):
        self.game: ConnectFour = game.clone()
        self.action: int = action
        self.parent: 'Node' = parent
        self.actions: list[int] = game.get_valid_moves()
        self.children: list = []
        self.payoff: int = 0
        self.visits: int = 0
    
    @property
    def q(self) -> float:
        return self.payoff / (self.num_paths or 1)