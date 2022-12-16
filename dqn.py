import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import math
import numpy as np
from game import Game
import random
import players

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.convolutional1 = nn.Conv2d(1, 32, kernel_size=5, padding=2)
        self.convolutional2 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.convolutional3 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.convolutional4 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.convolutional5 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.convolutional6 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.convolutional7 = nn.Conv2d(32, 32, kernel_size=5, padding=2)
        self.linear1 = nn.Linear(6 * 7 * 32, 50)
        self.linear2 = nn.Linear(50, 50)
        self.linear3 = nn.Linear(50, 50)
        self.linear4 = nn.Linear(50, 7)
        
    def forward(self, x):
        x = F.leaky_relu(self.convolutional1(x))
        x = F.leaky_relu(self.convolutional2(x))
        x = F.leaky_relu(self.convolutional3(x))
        x = F.leaky_relu(self.convolutional4(x))
        x = F.leaky_relu(self.convolutional5(x))
        x = F.leaky_relu(self.convolutional6(x))
        x = F.leaky_relu(self.convolutional7(x))
        x = x.view(x.size(0), -1)
        x = F.leaky_relu(self.linear1(x))
        x = F.leaky_relu(self.linear2(x))
        x = F.leaky_relu(self.linear3(x))
        x = self.linear4(x)
        return x

def select_action(policy_net, state, available_actions, steps_done=None, training=True):
    # batch and color channel
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    state = torch.tensor(np.array(state), dtype=torch.float, device=device).unsqueeze(dim=0).unsqueeze(dim=0)
    epsilon = random.random()
    if training:
        eps_threshold = 0.01 + (0.89) * math.exp(-1 * steps_done / 1000)
    else:
        eps_threshold = 0
    
    # follow epsilon-greedy policy
    if epsilon > eps_threshold:
        with torch.no_grad():
            # action recommendations from policy net
            r_actions = policy_net(state)[0, :]
            state_action_values = [r_actions[action].cpu() for action in available_actions]
            argmax_action = np.argmax(state_action_values)
            greedy_action = available_actions[argmax_action]
            return greedy_action
    else:
        return random.choice(available_actions)

def optimize_model(policy_net, target_net, replay_buffer):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if len(replay_buffer) < 256:
        return
    transitions = random.sample(replay_buffer, 256)
    state_batch, action_batch, reward_batch, next_state_batch = zip(*[(np.expand_dims(m[0], axis=0), \
                                        [m[1]], m[2], np.expand_dims(m[3], axis=0)) for m in transitions])
    # tensor wrapper
    state_batch = torch.tensor(np.array(state_batch), dtype=torch.float, device=device)
    action_batch = torch.tensor(np.array(action_batch), dtype=torch.long, device=device)
    reward_batch = torch.tensor(np.array(reward_batch), dtype=torch.float, device=device)
    
    # for assigning terminal state value = 0 later
    non_final_mask = torch.tensor(np.array(tuple(map(lambda s_: s_[0] is not None, next_state_batch))), device=device)
    non_final_next_state = torch.cat([torch.tensor(np.array(s_), dtype=torch.float, device=device).unsqueeze(0) for s_ in next_state_batch if s_[0] is not None])
    
    # prediction from policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    
    # truth from target_net, initialize with zeros since terminal state value = 0
    next_state_values = torch.zeros(256, device=device)
    # tensor.detach() creates a tensor that shares storage with tensor that does not require grad
    next_state_values[non_final_mask] = target_net(non_final_next_state).max(1)[0].detach()
    # compute the expected Q values
    expected_state_action_values = (next_state_values * 0.999) + reward_batch

    # Compute Huber loss
    loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1)) # torch.tensor.unsqueeze returns a copy
    optimizer = optim.Adam(policy_net.parameters())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

def win_rate_test(policy_net):
    win_moves_taken_list = []
    win = []
    mcts = players.MCTSPlayer(10000)
    for i in range(100):
        game = Game(6, 7)
        win_moves_taken = 0
        if i % 2:
            while not game.is_terminal:
                state = game.clone().board
                available_actions = game.get_valid_moves()
                action = select_action(policy_net, state, available_actions, training=False)
                reward = game.move(action)
                win_moves_taken += 1

                if reward == 1:
                    win_moves_taken_list.append(win_moves_taken)
                    win.append(1)
                    break

                available_actions = game.get_valid_moves()
                action = mcts.move(game, game.player_to_move)
                game.move(action)
        else:
            while not game.is_terminal:
                available_actions = game.get_valid_moves()
                action = mcts.move(game, game.player_to_move)
                game.move(action)
                
                state = game.clone().board
                available_actions = game.get_valid_moves()
                action = select_action(policy_net, state, available_actions, training=False)
                reward = game.move(action)
                win_moves_taken += 1

                if reward == 1:
                    win_moves_taken_list.append(win_moves_taken)
                    win.append(1)
                    break

    return sum(win)/100, sum(win_moves_taken_list)/len(win_moves_taken_list)
