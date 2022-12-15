class Board:

    WIDTH: int = 7
    HEIGHT: int = 6
    TOKENS: list = [
        [7, 4], # Horizontal Connect-Four
        [1, 2], # Vertical Connect-Four
        [6, 12], # Diagonal Connect-Four
        [8, 16] # Diagonal Connect-Four
    ]

    def __init__(self) -> None:
        '''
        position: bitstring representing the positions of the tokens of a player
        mask: bitstring representing the positions of both players
        '''
        self.position: int = 0
        self.mask: int = 0
        self.moves = 0
    
    def clone(self):
        result: Board = Board()
        result.position = self.position
        result.mask = self.mask
        result.moves = self.moves
        return result
    
    def is_playable(self, col: int) -> bool:
        top_mask: int = 1 << (Board.HEIGHT - 1) << col * (Board.HEIGHT + 1)
        return (self.mask & top_mask) == 0

    def connected_four(self) -> bool:
        line: int

        # Use the position bitboard to determine a win
        for [a, b] in Board.TOKENS:
            line = self.position & (self.position >> a)
            if (line & (line >> b)):
                return True

        return False
    
    def move(self, col: int) -> bool:
        if not (0 <= col < Board.WIDTH):
            raise ValueError
        
        if not self.is_playable(col):
            raise ValueError

        bottom_mask: int = 1 << (col * (Board.HEIGHT + 1))
        self.position ^= self.mask
        self.mask |= self.mask + bottom_mask
        self.moves += 1

        return self.connected_four()
    
    def get_valid_moves(self) -> list:
        return [c for c in range(Board.WIDTH) if self.is_playable(c)]