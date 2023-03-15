from mcts.node import Node
from game.connectfour import ConnectFour
from players.baseplayer import BasePlayer
import math
import random
import time

class MCTSPlayer(BasePlayer):

    def __init__(self, time_limit: float = 0.01):
        self.time_limit: float = time_limit        

    def move(self, game: ConnectFour):
        root = Node(game)
        player = game.player_to_move
        time_limit: float = time.time() + self.time_limit

        while time.time() < time_limit:
            curr_node = root

            # explore
            while not curr_node.game.is_terminal:

                # if we have no more legal moves left
                if len(curr_node.actions) != 0:
                    break

                ucbs = [] # UCB values of each child
                for child in curr_node.children:
                    UCB = child.q
                    val: float = math.sqrt(2) * math.sqrt(math.log(child.parent.visits) / child.visits)

                    if child.parent.game.player_to_move == ConnectFour.PLAYER_ONE:
                        UCB -= val
                    else:
                        UCB += val
                    
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

                else:
                    payoff = 1 if curr_state.game.winner == player else -1
                
                backprop_node: Node = next_node

            else:
                if curr_node.game.winner is None:
                    payoff = 0

                else:
                    payoff = 1 if curr_node.game.winner == player else -1
                
                backprop_node: Node = curr_node
            
            # backpropagation
            while(backprop_node is not None):
                backprop_node.visits += 1
                backprop_node.payoff += payoff
                backprop_node = backprop_node.parent

        exploitations = []
        for child in root.children:
            exploitations.append(child.payoff / child.visits)
        
        if(root.game.player_to_move == ConnectFour.PLAYER_ONE):
            i = exploitations.index(min(exploitations))
        else:
            i = exploitations.index(max(exploitations))

        return root.children[i].action