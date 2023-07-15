import pdb
from bitarray import bitarray

class Connect4():
    """Connect 4: 6 x 7 grid where players choose a column (1-7) and \ 
    the piece then falls until it hits another piece. One player wins when 
    four of the same color are in the grid either horizontal, vertical, or 
    diagonal."""
    def __init__(self):
        """Represent map as bitarray. 
        6 rows 7 columns so make each column is two bits, one for color and occupied. Total of 6 x 2 x 7 bits? """
        self.board_occupied = [bitarray("000000"), bitarray("000000"), bitarray("000000"), bitarray("000000"),bitarray("000000"), bitarray("000000"), bitarray("000000")]
        self.board_color = [bitarray("000000"), bitarray("000000"), bitarray("000000"), bitarray("000000"), bitarray("000000"), bitarray("000000"), bitarray("000000")]

        self.player = 1
        self.turn = 1


    def print_board(self):
        # x for player one, o for player two
        # transpose to print
        board_ = [[ '.' for s in range(0,7)] for t in range(0, 6)]

        for col, cval in enumerate(self.board_occupied):
            for row, rval in enumerate(cval):
                if cval[row] == 1:
                    # lookup color
                    if self.board_color[col][row] == 1:
                        board_[row][col] = 'x'
                    else:
                        board_[row][col] = 'o'
        print("\n".join(["".join([str(s) for s in t]) for t in board_]))
        print("\n\n")

    def is_full(self):
        """Checks if board is full."""
        if self.turn >= 6*7:
            return(True)
        else:
            return(False)

    def valid_move(self, move):
        """Checks if player can play selected column (full or not)."""
        if move == -1:
            return(False)

        if self.board_occupied[move].all():
            return(False)
        else:
            return(True)

    def update(self, move):
        """Takes a valid move and updates board."""
        if self.player == 1:
            marker = 'x'
        else:
            marker = 'o'
        # find first empty slot in column move
        idx = self.board_occupied[move].find(1)
        if idx == -1:
            idx = len(self.board_occupied[move]) - 1
        else:
            idx = idx - 1
        self.board_occupied[move][idx] = 1
        # update board_color
        # if 1 then 1 else 0
        if self.player == 1:
            self.board_color[move][idx] = 1
        else:
            self.board_color[move][idx] = 0

        # switch player
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def check_win(self):
        """Checks for wins in rows/columns/diagonals. Returns winning player and winning status (or continue game)."""
        def check_row_win(row, col):
            row_check_cols = set([0,1,2,3])

            # check if we need to check
            if col not in row_check_cols:
                return((None, False))

            # check if row is occupied
            this_row = [self.board_occupied[c][row] 
                        for c in range(col, col + 4)] 
                       
            if all(this_row):
                # check if all same color
                this_row_col = [self.board_color[c][row]
                                for c in range(col, col + 4)]

                if all(this_row_col):
                    #player 1 is winner
                    win_status = True
                    win_player = 1
                    return((win_player, win_status))

                # check if player 2
                this_row_col2 = [not v for v in this_row_col]
                if all(this_row_col2):
                    win_status = True
                    win_player = 2
                    return((win_player, win_status))

            return((None, False))

        def check_col_win(row, col):
            col_check_rows = set([0,1,2])
            win_status = False
            win_player = None
            
            if row not in col_check_rows:
                return((win_status, win_player))

            if all(self.board_occupied[col][row:(row + 4)]):
                if all(self.board_color[col][row:(row + 4)]):
                    win_status = True
                    win_player = 1
                    return((win_status, win_player))

                tmp = [v == 0 for v in self.board_color[col][row:(row + 4)]]
                if all(tmp):
                    win_status = True
                    win_player = 2
                    return((win_status, win_player))

            return((win_player, win_status))

        def check_rising_diagonal_win(row, col):
            up_diag_checks = {"rows": set([3,4,5]),
                              "cols": set([0,1,2,3])}
            win_status = False
            win_player = None

            if row in up_diag_checks["rows"] and col in up_diag_checks["cols"]:
                # check
                this_diag = [self.board_occupied[col + t][row - t] == 1 
                             for t in range(0, 4)]
                if all(this_diag):
                    this_col_diag = [self.board_color[col + t][row - t] == 1 
                             for t in range(0, 4)]
                    if all(this_col_diag):
                        win_player = 1
                        win_status = True
                        return((win_player, win_status))

                    this_col_diag2 = [not t for t in this_col_diag]
                    if all(this_col_diag2):
                        win_player = 2
                        win_status = True
                        return((win_player, win_status))
            else:
                return((win_player, win_status))

            return((win_player, win_status))

        def checks_falling_diagonal_win(row, col):
            down_diag_checks = {"rows": set([0,1,2]), 
                                "cols":set([0,1,2,3])}
            win_status = False
            win_player = None

            if row in down_diag_checks["rows"] and col in down_diag_checks["cols"]:
                this_diag = [self.board_occupied[col + t][row + t] == 1 
                             for t in range(0, 4)]
                if all(this_diag):
                    this_col_diag = [self.board_color[col + t][row + t] == 1 
                             for t in range(0, 4)]
                    if all(this_col_diag):
                        win_player = 1
                        win_status = True
                        return((win_player, win_status))

                    this_col_diag2 = [not t for t in this_col_diag]
                    if all(this_col_diag2):
                        win_player = 2
                        win_status = True
                        return((win_player, win_status))
            else:
                return((win_player, win_status))

            return((win_player, win_status))

        win_player = None
        win_status = False

        row_list_check1 = [[] for t in range(6)]
        row_list_check2 = [[] for t in range(6)]

        for col, cval in enumerate(self.board_occupied):
            for row, rval in enumerate(cval):
                win_player, win_status = check_row_win(row, col)
                if win_status:
                    return((win_player, win_status))

                win_player, win_status = check_col_win(row, col)
                if win_status:
                    return((win_player, win_status))

                win_player, win_status = check_rising_diagonal_win(row, col)
                if win_status:
                    return((win_player, win_status))

                win_player, win_status = checks_falling_diagonal_win(row, col)
                if win_status:
                    return((win_player, win_status))

        return((win_player, win_status))

    def play(self, display=True):
        end_of_game = False

        while not end_of_game:
            # check if full
            if self.is_full():
                end_of_game = True
                break
            current_player = self.player

            col = -1
            while not self.valid_move(col):
                if(display):
                    self.print_board()
                col = int(input("Player %d enter column: " % current_player))
                if self.valid_move(col):
                    print("player is %d." % self.player)
                    self.update(col)
                    self.turn += 1
                    win_player, win_status = self.check_win()
                    if win_status:
                        end_of_game = True
                        print("Player %d has won!" % win_player)
                    break


if __name__=="__main__":
    x = Connect4()
    x.play()
