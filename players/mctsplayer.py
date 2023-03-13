from mcts.node import Node
from game.connectfour import ConnectFour
from players.baseplayer import BasePlayer
import math
import random
import time

class MCTSPlayer(BasePlayer):

    def __init__(self, time_limit: float = 0.01):
        self.time_limit = time_limit

    def move(self, game, player):
        root = Node(game)
        time_end = time.time() + self.time_limit

        while time.time() < time_end:
            curr_node = root

            # explore
            while not curr_node.game.is_terminal:

                # if we have no more legal moves left
                if len(curr_node.actions) != 0:
                    break

                ucbs = [] # UCB values of each child
                for child in curr_node.children:
                    UCB = child.q

                    if child.parent.game.player_to_move == ConnectFour.PLAYER_ONE:
                        UCB -= 2 * math.sqrt(2) * math.sqrt(math.log(child.parent.num_paths) / child.num_paths)
                        # ucbs.append(child.q - 2 * math.sqrt(2) * math.sqrt(math.log(child.parent.num_paths) / child.num_paths))
                    else:
                        UCB += 2 * math.sqrt(2) * math.sqrt(math.log(child.parent.num_paths) / child.num_paths)
                        # ucbs.append(child.q + 2 * math.sqrt(2) * math.sqrt(math.log(child.parent.num_paths) / child.num_paths))
                    
                    ucbs.append(UCB)
                    
                if(curr_node.game.player_to_move == ConnectFour.PLAYER_ONE):
                    i = ucbs.index(min(ucbs))
                else:
                    i = ucbs.index(max(ucbs))
                
                # selection
                curr_node = curr_node.children[i]
            
            # expansion
            if not curr_node.game.is_terminal:
                action = curr_node.actions.pop()
                game_copy = curr_node.game
                game_copy.move(action)
                next_node = Node(game_copy, action, curr_node)
                curr_node.children.append(next_node)
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
                    tmp = tmp.parent
            else:
                if curr_node.game.winner is None:
                    payoff = 0
                elif curr_node.game.winner == player:
                    payoff = 1
                else:
                    payoff = -1
                
                # backpropagation
                tmp = curr_node
                while(tmp is not None):
                    tmp.num_paths += 1
                    tmp.payoff += payoff
                    tmp = tmp.parent

        exploitations = []
        for child in root.children:
            exploitations.append(child.payoff / child.num_paths)
        
        if(root.game.player_to_move == 1):
            i = exploitations.index(min(exploitations))
        else:
            i = exploitations.index(max(exploitations))

        return root.children[i].game_copy