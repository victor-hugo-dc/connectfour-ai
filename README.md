# Connect 4 MCTS and Deep Q-Network
Implementation of a Monte Carlo Tree Search algorithm and a Deep Q-Network for Connect Four. Made as a final project for *Computational Intelligence for Games*. The orginal code was written in a Jupyter notebook but has since been transferred to individual files for ease of use and modularity.

## Usage
To run this project,
1. Install Python 3.8 or above from [here](https://www.python.org/download/releases/)
2. Clone the repository:
    ```
    git clone https://github.com/victor-hugo-dc/connectfour-ai.git
    ```
    or download as a zip file and extract.
3. To install all dependencies, run:
    ```
    pip install -r requirements.txt
    ```
4. In `simulate.py`, view the possible simulations that can be made with the MCTS. Choose a match up, write it in the main file and in the root directory, run:
    ```
    python3 main.py
    ```
5. To run the DQN, go in the ai directory and run `train.py`
## Authors
- [Victor Del Carpio](https://github.com/victor-hugo-dc)
- [Rohan Acharya](https://github.com/roacharya)