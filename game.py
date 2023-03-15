class Game:
    EMPTY_CELL = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.board = [[Game.EMPTY_CELL for _ in range(cols)] for _ in range(rows)]
        self.player_to_move = 1
        self.is_terminal = False
        self.winner = None

    def clone(self):
        result = Game(self.rows, self.cols)
        result.board = [row[:] for row in self.board]
        return result

    # places the move in the correct column and updates the board,
    # if it cant be played then it returns an error, otherwise it
    # returns the boolean value of whether or not sequence of four
    # same colored disks for the input player is in the board
    def move(self, col: int) -> bool:
        
        if not (0 <= col < self.cols):
            raise ValueError(f'Poor column value: {col}')

        for row in range(self.rows):
            if self.board[row][col] == Game.EMPTY_CELL:
                self.board[row][col] = self.player_to_move
                self.player_to_move = 3 - self.player_to_move
                if len(self.get_valid_moves()) == 0:
                    self.is_terminal = True
                    return False
                if self.check_connect_four((row, col), 3 - self.player_to_move):
                    self.winner = 3 - self.player_to_move
                    self.is_terminal = True
                    return True
                else:
                    return False
                
        
        raise ValueError(f'Column {col} is full')
    
    # this checks if we have created a connect four by expanding from the current
    # position in each opposing direction, so we can check verticals, horizontals,
    # and both diagonals.
    def check_connect_four(self, position: tuple, player: int) -> bool:

        north = self._expand(position, (1, 0), player)
        south = self._expand(position, (-1, 0), player)

        vertical = north + south - 1
        if vertical >= 4:
            return True

        west = self._expand(position, (0, -1), player)
        east = self._expand(position, (0, 1), player)

        horizontal = west + east - 1
        if horizontal >= 4:
            return True

        northeast = self._expand(position, (1, 1), player)
        southwest = self._expand(position, (-1, -1), player)

        diag_nesw = northeast + southwest - 1
        if diag_nesw >= 4:
            return True

        northwest = self._expand(position, (1, -1), player)
        southeast = self._expand(position, (-1, 1), player)

        diag_nwse = northwest + southeast - 1
        if diag_nwse >= 4:
            return True

        return False


    # position is passed in as a tuple of (row, col)
    # player is either PLAYER_ONE or PLAYER_TWO
    def _expand(self, position: tuple, delta: tuple, player: int) -> int:
        row, col = position
        row_delta, col_delta = delta
        count: int = 0

        # i think we cna remove the try catch finally now that were checking
        # for the bounds (this was taken from the other code)
        try:
            while (0 <= row < self.rows) and (0 <= col < self.cols) \
                and self.board[row][col] == player:

                count += 1
                row += row_delta
                col += col_delta
        
        finally:
            return count


    # if you think about it we only have to check the last value of each row
    # to know what columns are available to be played on
    def get_valid_moves(self):
        return [i for i, v in enumerate(self.board[self.rows - 1]) if v == Game.EMPTY_CELL]