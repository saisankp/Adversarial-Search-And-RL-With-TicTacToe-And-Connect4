import random


class DefaultOpponent:

    @staticmethod
    def make_next_tic_tac_toe_move(**kwargs):
        default_opponent = kwargs.get('self', None)
        tictactoe_board = kwargs.get('board', None)
        move_to_win = default_opponent.move_to_win_tic_tac_toe(tictactoe_board, tictactoe_board.turn)
        if move_to_win is not None:
            return move_to_win
        move_to_block_opponent = default_opponent.move_to_block_opponent_winning_tic_tac_toe(tictactoe_board, tictactoe_board.turn)
        if move_to_block_opponent is not None:
            return move_to_block_opponent
        return random.choice(tictactoe_board.possible_moves())

    @staticmethod
    def move_to_win_tic_tac_toe(tictactoe_board, you):
        # Assignment spec asks for the default opponent to "be better than fully random"
        # This function has been designed to mimic a human opponent
        winning_move = None
        for possible_move in tictactoe_board.possible_moves():
            potential_tictactoe_board_to_win = tictactoe_board.copy()
            potential_tictactoe_board_to_win.push(tuple(possible_move))
            if potential_tictactoe_board_to_win.result() == you:
                if random.uniform(0, 1) < 0.01:
                    # 1% of the time, it will be close to "perfect"
                    winning_move = possible_move
                else:
                    # Remainder of the time, it will not be close to "perfect"
                    random.choice(tictactoe_board.possible_moves())
                break
        return winning_move

    @staticmethod
    def move_to_block_opponent_winning_tic_tac_toe(tictactoe_board, you):
        # Assignment spec asks for the default opponent to "be better than fully random"
        # This function has been designed to mimic a human opponent
        blocking_move = None
        opponent = you % 2 + 1
        for possible_move in tictactoe_board.possible_moves():
            potential_tictactoe_board_to_win = tictactoe_board.copy()
            potential_tictactoe_board_to_win.set_mark(possible_move.tolist(), opponent)
            if potential_tictactoe_board_to_win.result() == opponent:
                if random.uniform(0, 1) < 0.01:
                    # 1% of the time, it will be close to "perfect"
                    blocking_move = possible_move
                else:
                    # Remainder of the time, it will not be close to "perfect"
                    random.choice(tictactoe_board.possible_moves())
                break
        return blocking_move

    @staticmethod
    def make_next_connect_four_move(**kwargs):
        default_opponent = kwargs.get('self', None)
        connect_four_board = kwargs.get('board', None)
        move_to_win = default_opponent.move_to_win_connect_four(connect_four_board, connect_four_board.turn)
        if move_to_win is not None:
            return move_to_win
        move_to_block_opponent = default_opponent.move_to_block_opponent_winning_connect_four(connect_four_board, connect_four_board.turn)
        if move_to_block_opponent is not None:
            return move_to_block_opponent
        return random.choice(connect_four_board.possible_moves())

    @staticmethod
    def move_to_win_connect_four(connect_four_board, turn):
        # Assignment spec asks for the default opponent to "be better than fully random"
        # This function has been designed to mimic a human opponent
        winning_move = None
        # Iterate through all possible moves and choose one that makes you win!
        for possible_move in connect_four_board.possible_moves():
            potential_connect_four_board_to_win = connect_four_board.copy()
            potential_connect_four_board_to_win.push(possible_move)
            if potential_connect_four_board_to_win.result() == turn:
                if random.uniform(0, 1) < 0.01:
                    # 1% of the time, it will be close to "perfect"
                    winning_move = possible_move
                else:
                    # Remainder of the time, it will not be close to "perfect"
                    random.choice(connect_four_board.possible_moves())
                break
        return winning_move

    @staticmethod
    def move_to_block_opponent_winning_connect_four(connect_four_board, you):
        blocking_move = None
        # Alternate turns for you vs opponent
        opponent = you % 2 + 1
        # Iterate through all possible moves your opponent can use and do their winning move before them!
        for move in connect_four_board.possible_moves():
            potential_connect_four_board_to_win = connect_four_board.copy()
            potential_connect_four_board_to_win.set_mark((move, max(connect_four_board.state_dict[move])), opponent)
            if potential_connect_four_board_to_win.result() == opponent:
                if random.uniform(0, 1) < 0.01:
                    # 1% of the time, it will be close to "perfect"
                    blocking_move = move
                else:
                    # Remainder of the time, it will not be close to "perfect"
                    random.choice(connect_four_board.possible_moves())
                break
        return blocking_move
