class Board:

    def __init__(self, board, move=None):
        self.board = board
        if move:
            self.move = move
            self.make_move(move[0], move[1], move[2])

    def get_move(self):
        return self.move

    def current_board(self):
        return self.board #List-style 
    
    def print_board(self):
        print('-' * 67)
        print('\t0\t1\t2\t3\t4\t5\t6\t7\n')
        for idx, row in enumerate(self.board):
            row_string = '{}'.format(idx)
            for r in row:
                row_string += '\t{}'.format(r)
            print(row_string)
            print('')

    def in_range(self, move):
        return (int(move) > 0 and int(move) < 8)

    def show_valid_moves(self, turn, output=True):
        # turn, even - black, odd - white
        player = 'B' if (turn % 2 == 0) else 'W'
        opponent = 'B' if (turn % 2 == 1) else 'W'
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == player:
                    if (r-1) >= 0 and self.board[r - 1][c] == opponent:
                        for i in range(r-1, 0, -1):
                            if self.board[i-1][c] == 'x' or self.board[i-1][c] == player:
                                break
                            if self.board[i-1][c] == '.':
                                self.board[i-1][c] = 'x'
                                valid_moves.append((i-1, c))
                                break
                    if (r+1) < 8 and self.board[r + 1][c] == opponent:
                        for i in range(r+1,8):
                            if self.board[i][c] == 'x' or self.board[i][c] == player:
                                break
                            if self.board[i][c] == '.':
                                self.board[i][c] = 'x'
                                valid_moves.append((i, c))
                                break
                    if (c-1) >= 0 and self.board[r][c - 1] == opponent:
                        for i in range(c-1, 0, -1):
                            if self.board[r][i-1] == 'x' or self.board[r][i-1] == player:
                                break
                            if self.board[r][i-1] == '.':
                                self.board[r][i-1] = 'x'
                                valid_moves.append((r, i-1))
                                break
                    if (c+1) < 8 and self.board[r][c + 1] == opponent:
                        for i in range(c+1, 8):
                            if self.board[r][i] == 'x' or self.board[r][i] == player:
                                break
                            if self.board[r][i] == '.':
                                self.board[r][i] = 'x'
                                valid_moves.append((r, i))
                                break
                            
                    if (r-1) >= 0 and (c-1) >= 0 and self.board[r - 1][c - 1] == opponent:
                        for i in range(2,8):
                            if (r-i) >= 0 and (c-i) >= 0:
                                if self.board[r-i][c-i] == 'x' or self.board[r-i][c-i] == player:
                                    break
                                if self.board[r - i][c - i] == '.':
                                    self.board[r - i][c - i] = 'x'
                                    valid_moves.append((r-i, c-i))
                                    break
                            else: 
                                break
                    if (r-1) >= 0 and (c+1) < 8 and self.board[r - 1][c + 1] == opponent:
                        for i in range(2,8):
                            if (r-i) >= 0 and (c+i) < 8:
                                if self.board[r-i][c+i] == 'x' or self.board[r-i][c+i] == player:
                                    break
                                if self.board[r - i][c + i] == '.':
                                    self.board[r - i][c + i] = 'x'
                                    valid_moves.append((r-i, c+i))
                                    break
                            else: 
                                break
                    if (r+1) < 8 and (c-1) >= 0 and self.board[r + 1][c - 1] == opponent:
                        for i in range(2,8):
                            if (r+i) < 8 and (c-i) >= 0:
                                if self.board[r+i][c-i] == 'x' or self.board[r+i][c-i] == player:
                                    break
                                if self.board[r + i][c - i] == '.':
                                    self.board[r + i][c - i] = 'x'
                                    valid_moves.append((r+i, c-i))
                                    break
                            else:
                                break
                    if (r+1) < 8 and (c+1) < 8 and self.board[r + 1][c + 1] == opponent:
                        for i in range(2,8):
                            if (r+i) < 8 and (c+i) < 8:
                                if self.board[r+i][c+i] == 'x' or self.board[r+i][c+i] == player:
                                    break
                                if self.board[r + i][c + i] == '.':
                                    self.board[r + i][c + i] = 'x'
                                    valid_moves.append((r+i, c+i))
                                    break
                            else: 
                                break
        if output:
            self.print_board()

        return valid_moves

    def reset_board(self):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 'x':
                    self.board[r][c] = '.'

    def make_move(self, r, c, turn):
        player = 'B' if (turn % 2 == 0) else 'W'
        opponent = 'B' if (turn % 2 == 1) else 'W'
        # print('{} is making the move ({}, {})'.format(player, r, c))

        self.board[r][c] = player

        if (r - 1) >= 0 and self.board[r - 1][c] == opponent and self.in_row(r, c, player):
            for i in range(r - 1, 0, -1):
                if self.board[i][c] == opponent:
                    self.board[i][c] = player
                else:
                    break
        if (c - 1) >= 0 and self.board[r][c - 1] == opponent and self.in_col(r, c, player):
            for i in range(c - 1, 0, -1):
                if self.board[r][i] == opponent:
                    self.board[r][i] = player
                else:
                    break
        if (r + 1) < 8 and self.board[r + 1][c] == opponent and self.in_row(r, c, player, incr=True):
            for i in range(r + 1, 8):
                if self.board[i][c] == opponent:
                    self.board[i][c] = player
                else:
                    break
        if (c + 1) < 8 and self.board[r][c + 1] == opponent and self.in_col(r, c, player, incr=True):
            for i in range(c + 1, 8):
                if self.board[r][i] == opponent:
                    self.board[r][i] = player
                else:
                    break
        if (r - 1) >= 0 and (c - 1) >= 0 and self.board[r - 1][c - 1] == opponent and self.upper_left_diagonal(r, c, player):
            for i in range(1, 8):
                if (r - i) >= 0 and (c - i) >= 0:
                    if self.board[r - i][c - i] == opponent:
                        self.board[r - i][c - i] = player
                    else:
                        break
                else:
                    break
        if (r - 1) >= 0 and (c + 1) < 8 and self.board[r - 1][c + 1] == opponent and self.upper_right_diagonal(r, c, player):
            for i in range(1, 8):
                if (r - i) >= 0 and (c + i) < 8:
                    if self.board[r - i][c + i] == opponent:
                        self.board[r - i][c + i] = player
                    else:
                        break
                else:
                    break
        if (r + 1) < 8 and (c - 1) >= 0 and self.board[r + 1][c - 1] == opponent and self.lower_left_diagonal(r, c, player):
            for i in range(1, 8):
                if (r + i) < 8 and (c - i) >= 0:
                    if self.board[r + i][c - i] == opponent:
                        self.board[r + i][c - i] = player
                    else:
                        break
                else:
                    break
        if (r + 1) < 8 and (c + 1) < 8 and self.board[r + 1][c + 1] == opponent and self.lower_right_diagonal(r, c, player):
            for i in range(1, 8):
                if (r + i) < 8 and (c + i) < 8:
                    if self.board[r + i][c + i] == opponent:
                        self.board[r + i][c + i] = player
                    else:
                        break
                else:
                    break

    def in_row(self, r, c, player, incr=False):
        if incr:
            for row in range(r + 1, 8):
                if self.board[row][c] == player:
                    return True
        else:
            for row in range(r - 1, -1, -1):
                if self.board[row][c] == player:
                    return True
        return False

    def in_col(self, r, c, player, incr=False):
        if incr:
            for col in range(c + 1, 8):
                if self.board[r][col] == player:
                    return True
        else:
            for col in range(c - 1, -1, -1):
                if self.board[r][col] == player:
                    return True
        return False

    def upper_right_diagonal(self, r, c, player):
        # row neg, col pos
        for i in range(2, 8):
            if (r - i) >= 0 and (c + i) < 8:
                if self.board[r - i][c + i] == player:
                    return True
            else:
                return False
        return False

    def lower_right_diagonal(self, r, c, player):
        #both pos
        for i in range(2, 8):
            if (r + i) < 8 and (c + i) < 8:
                if self.board[r + i][c + i] == player:
                    return True
            else:
                return False
        return False

    def upper_left_diagonal(self, r, c, player):
        # both neg
        for i in range(2, 8):
            if (r - i) >= 0 and (c - i) >= 0:
                if self.board[r - i][c - i] == player:
                    return True
            else:
                return False
        return False

    def lower_left_diagonal(self, r, c, player):
        # row pos, col neg
        for i in range(2, 8):
            if (r + i) < 8 and (c - i) >= 0:
                if self.board[r + i][c - i] == player:
                    return True
            else:
                return False
        return False

    def print_nbr_of_tiles(self):
        w = 0
        b = 0
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == 'W':
                    w += 1
                if self.board[r][c] == 'B':
                    b += 1
        print('White tiles: {}'.format(w))
        print('Black tiles: {}'.format(b))
        return (b, w)

    def win_condition(self, valid_moves):
        print(valid_moves)
        if not valid_moves:
            return True
        return False