import math
import board
from copy import deepcopy

class Alphabeta:

    def __init__(self, color):
        self.color = color
        self.action = ''
        self.turn = 0
        
    def alphabeta_pruning(self, node, depth, alpha, beta, maximizing_player):
        self.set_turn(maximizing_player)
        # print('Alphabeta, node: {}, depth : {}, alpha: {}, beta: {}, maximizing: {}'.format(node, depth, alpha, beta, maximizing_player))
        if depth == 0 or self.terminal_state(node):
            return self.heuristic(node)
        if maximizing_player:
            v = -math.inf
            
            node.reset_board()
            valid_moves = node.show_valid_moves(self.turn, output=False)
            
            children = [board.Board(deepcopy(node.current_board()), 
                (valid_moves[i][0], valid_moves[i][1], self.turn)) for i in range(len(valid_moves))]
            
            for i, child in enumerate(children):
                v = max(v, self.alphabeta_pruning(child, depth - 1, alpha, beta, False))
                self.action = valid_moves[i]
                alpha = max(alpha, v)
                if alpha >= beta:
                    break # Beta cut-off
            return v
        else:
            v = math.inf

            node.reset_board()
            valid_moves = node.show_valid_moves(self.turn, output=False)

            children = [board.Board(deepcopy(node.current_board()), 
                (valid_moves[i][0], valid_moves[i][1], self.turn)) for i in range(len(valid_moves))]
            
            for i, child in enumerate(children):
                v = min(v, self.alphabeta_pruning(child, depth - 1, alpha, beta, True))
                self.action = valid_moves[i]
                beta = min(beta, v)
                if alpha >= beta:
                    break #Alpha cut-off
            return v

    def terminal_state(self, node):
        node.reset_board()
        valids = node.show_valid_moves(self.turn, output=False)
        if not valids:
            return True
        return False

    def heuristic(self, node):
        board_list = node.current_board()
        b = 0
        w = 0
        for r in range(8):
            for c in range(8):
                if board_list[r][c] == 'W':
                    w += 1
                elif board_list[r][c] == 'B':
                    b += 1
        if self.color == 'white':
            return w - b
        elif self.color == 'black':
            return b - w
    
    def get_action(self):
        return self.action
    
    def set_turn(self, maximizing_player):
        if maximizing_player:
            self.turn = 1 if self.color == 'white' else 0
        else:
            self.turn = 0 if self.color == 'white' else 1