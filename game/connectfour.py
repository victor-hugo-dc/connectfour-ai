import numpy as np
from copy import deepcopy

class ConnectFour:

    EMPTY_CELL = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    ROWS = 6
    COLS = 7

    def __init__(self, state: np.ndarray = None) -> None:
        self.board: np.ndarray

        if state is None:
            self.board = np.zeros((self.ROWS, self.COLS))
        else:
            self.board = deepcopy(state)
        
        self.player_to_move: int = ConnectFour.PLAYER_ONE
        self.is_terminal: bool = False
        self.winner: int = None

    def clone(self) -> 'ConnectFour':
        '''
        Returns a copy of the current ConnectFour object
        '''
        result = ConnectFour(self.board)
        result.player_to_move = self.player_to_move
        result.is_terminal = self.is_terminal
        result.winner = self.winner
        return result

    def switch_player(self) -> None:
        '''
        Alternate the player
        '''
        self.player_to_move = 3 - self.player_to_move

    def move(self, col: int) -> bool:
        '''
        Have the current player play the move at the column
        '''
        
        if not (0 <= col < self.COLS) or len(self.get_valid_moves()) == 0:
            raise ValueError(f'Poor column value: {col}')

        for row in range(self.ROWS):
            if self.board[row][col] == ConnectFour.EMPTY_CELL:

                self.board[row][col] = self.player_to_move

                if self.check_connect_four((row, col)):
                    self.winner = self.player_to_move
                    self.is_terminal = True
                    return True
                
                else:
                    if len(self.get_valid_moves()) == 0:
                        self.is_terminal = True
                    
                    self.switch_player()
                    
                return False
                
        
        raise ValueError(f'Column {col} is full')
    

    def check_connect_four(self, position: tuple) -> bool:
        '''
        Determine if there four-in-a-row by expanding from the most current played move
        '''

        directions = [
            [(1, 0), (-1, 0)],
            [(0, -1), (0, 1)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]

        for [one, two] in directions:
            if self._expand(position, one) + self._expand(position, two) - 1 >= 4:
                return True
 
        return False

    def _expand(self, position: tuple, delta: tuple) -> int:
        row: int
        col: int
        rdelta: int
        cdelta: int

        row, col = position
        rdelta, cdelta = delta
        count: int = 0

        while (0 <= row < self.ROWS) and (0 <= col < self.COLS) \
                and self.board[row][col] == self.player_to_move:

            count += 1
            row += rdelta
            col += cdelta
        
        return count


    def get_valid_moves(self):
        return [i for i, v in enumerate(self.board[self.ROWS - 1]) if v == ConnectFour.EMPTY_CELL]
    