import math
import board
import alphabeta

if __name__ == "__main__":
    player = input('Enter your play color (black/white): ')
    if not (player.lower() == 'black' or player.lower() == 'white'):
        print('Not a viable option')
        exit()

    board_list = [['.' for row in range(8)] for col in range(8)]

    board_list[3][3] = 'W'
    board_list[4][4] = 'W'
    board_list[3][4] = 'B'
    board_list[4][3] = 'B'

    my_board = board.Board(board_list)
    
    valid_moves = my_board.show_valid_moves(0, output=False)
    my_board.reset_board()

    ai_player = alphabeta.Alphabeta('black' if player == 'white' else 'white')

    turn = -1
    while True:
        turn += 1
        color_turn = 'Black' if (turn % 2 == 0) else 'White'
        valid_moves = my_board.show_valid_moves(turn)
        print(valid_moves)
        placed_move = False
        while not placed_move:
            print('-' * 67)
            print('{} turn!'.format(color_turn))
            if player == color_turn.lower():
                move = input('Pick your move (row, column) : ').split(',')
                if not len(move) == 2:
                    print('Wrong input, input should be e.g. 2,3')
                if move[0].isdigit() and move[1].isdigit():
                    r = int(move[0])
                    c = int(move[1])
                    if (r,c) in valid_moves:
                        my_board.make_move(r, c, turn)
                        placed_move = True
                    else:
                        print('Not a valid move, try again')
            else:
                print('---- AI ----')
                v = ai_player.alphabeta_pruning(my_board, 4, -math.inf, math.inf, True)
                action = ai_player.get_action()
                print('Action: {}, with value: {}'.format(action, v))
                my_board.make_move(action[0], action[1], turn)
                placed_move = True
                print('---- END ----')

        tile_tuple = my_board.print_nbr_of_tiles()
        my_board.reset_board()
        valid_moves = my_board.show_valid_moves(turn+1, output=False)
        my_board.reset_board()
        if not valid_moves:
            break
    
    winner = 'Black' if (tile_tuple[0] > tile_tuple[1]) else 'White'
    tile_tuple = tile_tuple if (tile_tuple[0] > tile_tuple[1]) else (tile_tuple[1], tile_tuple[0])
    print('The winner is: {} with: {} tiles vs {} tiles'.format(winner, tile_tuple[0], tile_tuple[1]))
        