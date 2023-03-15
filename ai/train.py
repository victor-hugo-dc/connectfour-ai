from game.connectfour import ConnectFour
from itertools import count
from dqn import DQN, select_action, optimize_model, win_rate_test
from players.randomplayer import RandomPlayer
from players.mctsplayer import MCTSPlayer
from players.dqnplayer import DQNPlayer
import torch
import numpy as np
from simulate import run_simulation

if __name__ == "__main__":
    try:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        replay_buffer = []

        policy_net = DQN().to(device)

        target_net = DQN().to(device)
        target_net.load_state_dict(policy_net.state_dict())
        target_net.eval()

        print("Training DQN -------------------")
        steps_done = 0
        training_history = []
        num_episodes = 20000
        TARGET_UPDATE = 10
        mcts = MCTSPlayer(10000)
        for i in range(num_episodes): 
            game = ConnectFour()
            state_p1 = game.clone().board

            # record every 20 epochs
            if i % 20 == 19:
                win_rate, moves_taken = win_rate_test(policy_net)
                training_history.append([i + 1, win_rate, moves_taken])
                th = np.array(training_history)
                # print training message every 200 epochs
                if i % 1 == 0:
                    torch.save(policy_net, "model" + str(i))
                    print('Episode {}: | win_rate: {} | moves_taken: {}'.format(i, th[-1, 1], th[-1, 2]))
            for t in count():
                available_actions = game.get_valid_moves()
                action_p1 = select_action(policy_net, state_p1, available_actions, steps_done)
                steps_done += 1
                state_p1_ = game.board
                reward_p1 = game.move(action_p1)

                if game.is_terminal:
                    if reward_p1 == 1:
                        # reward p1 for p1's win
                        replay_buffer.append([state_p1, action_p1, 1, None])
                    else:
                        # state action value tuple for a draw
                        replay_buffer.append([state_p1, action_p1, 0.5, None])
                    break

                available_actions = game.get_valid_moves()
                action_p2 = action = mcts.move(game, game.player_to_move)
                state_p2_ = game.board
                reward_p2 = game.move(action_p2)

                if game.is_terminal:
                    if reward_p2 == 1:
                        # punish p1 for (random agent) p2's win 
                        replay_buffer.append([state_p1, action_p1, -1, None])
                    else:
                        # state action value tuple for a draw
                        replay_buffer.append([state_p1, action_p1, 0.5, None])
                    break

                # punish for taking too long to win
                replay_buffer.append([state_p1, action_p1, -0.05, state_p2_])
                state_p1 = state_p2_

                # Perform one step of the optimization (on the policy network)
                optimize_model(policy_net, target_net, replay_buffer)

            # update the target network, copying all weights and biases in DQN
            if i % TARGET_UPDATE == TARGET_UPDATE - 1:
                target_net.load_state_dict(policy_net.state_dict())
    except KeyboardInterrupt:
        print('Training Complete')

        print("Test Results:")

        p1 = DQNPlayer(policy_net)
        p2 = RandomPlayer()
        wins = run_simulation(1000, [p1, p2])
        print("Win rate out of 1000 games of DQN against random player: " + str(wins[p1] / 10) + "%")

        p1 = DQNPlayer(policy_net)
        p2 = MCTSPlayer(1000)
        wins = run_simulation(1000, [p1, p2])
        print("Win rate out of 1000 games of DQN against MCTS: " + str(wins[p1] / 10) + "%")