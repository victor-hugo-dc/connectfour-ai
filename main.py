from players.randomplayer import RandomPlayer
from players.mctsplayer import MCTSPlayer
from game.connectfour import ConnectFour


def run_simulation(iterations, players):
    wins = {}
    wins[players[0]] = 0
    wins[players[1]] = 0
    
    for i in range(iterations):
        if i != 0 and i % 100 == 0:
            print(f"{i} games simulated")
            print(f"Player 1: {wins[players[0]]}")
            print(f"Player 2: {wins[players[1]]}")
            print("-" * 15)
            
        game = ConnectFour()
        # alternate who goes first
        if i % 2:
            game.player_to_move = ConnectFour.PLAYER_TWO

        while not game.is_terminal:
            player = players[game.player_to_move - 1]
            action = player.move(game)
            if game.move(action):
                wins[player] += 1
                break
    return wins

def mcts_random():
    p1 = MCTSPlayer(0.01)
    p2 = RandomPlayer()
    wins = run_simulation(1000, [p1, p2])
    print("Player 1 wins: " + str(wins[p1]))
    print("Player 2 wins: " + str(wins[p2]))
    print("Draws: " + str(1000 - wins[p1] - wins[p2]))

def mcts_mcts():
    p1 = MCTSPlayer(0.05)
    p2 = MCTSPlayer(0.01)
    wins = run_simulation(1000, [p1, p2])
    print("Player 1 wins: " + str(wins[p1]))
    print("Player 2 wins: " + str(wins[p2]))
    print("Draws: " + str(1000 - wins[p1] - wins[p2]))

def random_random():
    p1 = RandomPlayer()
    p2 = RandomPlayer()
    wins = run_simulation(1000, [p1, p2])
    print("Player 1 wins: " + str(wins[p1]))
    print("Player 2 wins: " + str(wins[p2]))
    print("Draws: " + str(1000 - wins[p1] - wins[p2]))


if __name__ == '__main__':
    mcts_random()