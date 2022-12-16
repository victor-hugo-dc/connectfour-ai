from abc import ABC, abstractmethod
import random
import dqn

class BasePlayer:
    def __init__(self):
        pass
    @abstractmethod
    def move(self, game, player):
        pass

class RandomPlayer(BasePlayer):
    def __init__(self):
        pass

    def move(self, game, player):
        return random.choice(game.get_valid_moves())

class Node:
    def __init__(self, game, game_copy, predecessor):
        self.game = game 
        self.game_copy = game_copy
        self.predecessor = predecessor
        self.actions = game.get_valid_moves()
        self.successors = []
        self.payoff = 0
        self.num_paths = 0

class MCTSPlayer(BasePlayer):
    def __init__(self, iterations):
        self.iterations = iterations

    def move(self, game, player):
        game_cpy = game.clone()
        root = Node(game_cpy, None, None)
        for i in range(self.iterations):
            curr_node = root
            while not curr_node.game.is_terminal:
                if len(curr_node.actions) != 0:
                    break
                vals = []
                for successor in curr_node.successors:
                    if successor.predecessor.game.player_to_move == 1:
                        vals.append(successor.payoff / successor.num_paths - 2 * math.sqrt(2) * math.sqrt(math.log(successor.predecessor.num_paths) / successor.num_paths))
                    else:
                        vals.append(successor.payoff / successor.num_paths + 2 * math.sqrt(2) * math.sqrt(math.log(successor.predecessor.num_paths) / successor.num_paths))
                if(curr_node.game.player_to_move == 1):
                    i = vals.index(min(vals))
                else:
                    i = vals.index(max(vals))
                curr_node = curr_node.successors[i]
            if not curr_node.game.is_terminal:
                action = curr_node.actions.pop()
                game_copy = curr_node.game
                game_copy.move(action)
                next_node = Node(game_copy, action, curr_node)
                curr_node.successors.append(next_node)
                curr_state = next_node
                while not curr_state.game.is_terminal:
                    action = random.choice(curr_state.actions)
                    game_copy = curr_node.game
                    game_copy.move(action)
                    new_state = Node(game_copy, action, curr_state)
                    curr_state = new_state
                if curr_state.game.winner is None:
                    payoff = 0
                elif curr_state.game.winner == player:
                    payoff = 1
                else:
                    payoff = -1
                tmp = next_node
                while(tmp is not None):
                    tmp.num_paths += 1
                    tmp.payoff += payoff
                    tmp = tmp.predecessor
            else:
                if curr_node.game.winner is None:
                    payoff = 0
                elif curr_node.game.winner == player:
                    payoff = 1
                else:
                    payoff = -1
                tmp = curr_node
                while(tmp is not None):
                    tmp.num_paths += 1
                    tmp.payoff += payoff
                    tmp = tmp.predecessor
        exploitations = []
        for successor in root.successors:
            exploitations.append(successor.payoff / successor.num_paths)
        if(root.game.player_to_move == 1):
            i = exploitations.index(min(exploitations))
        else:
            i = exploitations.index(max(exploitations))
        return root.successors[i].game_copy          

class DQNPlayer(BasePlayer):
    def __init__(self, policy_net):
        self.policy_net = policy_net

    def move(self, game, player):
        return dqn.select_action(self.policy_net, game.board, game.get_valid_moves(), training=False)