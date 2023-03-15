from players.baseplayer import BasePlayer
from game.connectfour import ConnectFour
from ai import dqn

class DQNPlayer(BasePlayer):
    def __init__(self, policy_net):
        self.policy_net = policy_net

    def move(self, game: ConnectFour):
        return dqn.select_action(self.policy_net, game.board, game.get_valid_moves(), training=False)