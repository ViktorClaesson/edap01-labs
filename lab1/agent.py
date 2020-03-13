import math
from copy import deepcopy

class Agent:

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.actions = []
    
    def set_actions(self, actions): # Called from main, valid_moves 
        self.actions = actions
    

    def alphabeta_search(self, state, actions, depth, alpha, beta, maximizing_player):
        if depth == 0 or not actions:
            return self.utility(state)
        if maximizing_player:
            v = -math.inf
            for a in actions:
                v = max(v, self.alphabeta_search(state, a, depth - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if alpha >= beta:
                    break
            return v
        else:
            v = math.inf
            for a in actions:
                v = min(v, self.alphabeta_search(state, a, depth - 1, alpha, beta, True))
                beta = min(beta, v)
                if alpha >= beta:
                    break
            return v

    def alpha_beta_search(self, state, depth):
        print('alpha-beta-search')
        print(self.actions)
        v = self.max_value(state, -math.inf, math.inf, depth, True)
        return self.actions[v]

    def max_value(self, state, alpha, beta, depth, maximizing_player):
        print('max-value')
        if self.terminal_test(state, depth):
            return self.utility(state)
        v = -math.inf
        for a in self.actions:
            v = max(v, self.min_value(self.result(state, a), alpha, beta, depth - 1, False))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth, maximizing_player):
        print('min-value')
        if self.terminal_test(state, depth):
            return self.utility(state)
        v = math.inf
        for a in self.actions:
            v = min(v, self.max_value(self.result(state, a), alpha, beta, depth - 1, True))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def utility(self, state):
        b, w = self.count_tiles(state)
        if b == w:
            return 0
        elif self.color == 'B':
            return 1 if (b > w) else -1
        elif self.color == 'W':
            return 1 if (w > b) else -1

    def terminal_test(self, state, depth):
        #Check if game is over
        if not state:
            return True
        if depth == 0:
            return True
        return False

    def result(self, state, action):
        print('result')
        # if we do the action, action, in state, state, how will the resulting 
        # state look like in comparison to the given state.
        tmp_board = deepcopy(state)
        color = 0 if (self.color == 'B') else 1
        print(tmp_board)
        print(action)
        self.board.make_move(action[0], action[1], int(color))
        print(tmp_board)
        b, w = self.count_tiles(state)
        b_updated, w_updated = self.count_tiles(tmp_board)

        if self.color == 'B':
            return ((b_updated - b) - (w_updated - w))
        return tmp_board

    def count_tiles(self, board):
        w = 0
        b = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == 'W':
                    w += 1
                if board[r][c] == 'B':
                    b += 1
        return b, w

if __name__ == "__main__":
    pass