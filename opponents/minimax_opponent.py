import math


class MinimaxOpponent:
    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    @staticmethod
    def minimax_for_tic_tac_toe(self, tictactoe_board, alpha, beta, maximize):
        result = tictactoe_board.result()
        if result == 1:
            return 1, None
        if result == 2:
            return -1, None
        elif result == 0:
            return 0, None
        if maximize:
            best_move = None
            maximum_evaluation_value = -100
            for possible_move in tictactoe_board.possible_moves():
                temporary_tictactoe_board = tictactoe_board.copy()
                temporary_tictactoe_board.push(possible_move)
                evaluation = self.minimax_for_tic_tac_toe(self, temporary_tictactoe_board, alpha, beta, False)[0]
                if evaluation > maximum_evaluation_value:
                    best_move = possible_move
                    maximum_evaluation_value = evaluation
                if alpha is not None:
                    alpha = max(alpha, maximum_evaluation_value)
                    if alpha >= beta:
                        break
            return maximum_evaluation_value, best_move
        elif not maximize:
            best_move = None
            minimum_evaluation_value = 100
            for possible_move in tictactoe_board.possible_moves():
                temporary_tictactoe_board = tictactoe_board.copy()
                temporary_tictactoe_board.push(possible_move)
                evaluation = self.minimax_for_tic_tac_toe(self, temporary_tictactoe_board, alpha, beta, True)[0]
                if evaluation < minimum_evaluation_value:
                    best_move = possible_move
                    minimum_evaluation_value = evaluation
                if beta is not None:
                    beta = min(beta, minimum_evaluation_value)
                    if alpha >= beta:
                        break
            return minimum_evaluation_value, best_move

    @staticmethod
    def make_next_tic_tac_toe_move(**kwargs):
        self = kwargs.get('self', None)
        board = kwargs.get('board', None)
        _, move = self.minimax_for_tic_tac_toe(self, board, self.alpha, self.beta, board.turn == 1)
        return move


    @staticmethod
    def minimax_for_connect_four(self, connect_four_board, depth_limit, alpha, beta, maximize):
        result = connect_four_board.result()
        if (connect_four_board.has_won(1) or connect_four_board.has_won(2)) or depth_limit == 0:
            if result == 1:
                return 1, None
            if result == 2:
                return -1, None
            elif result == 0:
                return 0, None
            return 0, None
        if maximize:
            best_move = None
            maximum_evaluation_value = -math.inf
            for possible_move in connect_four_board.possible_moves():
                temporary_connect_four_board = connect_four_board.copy()
                temporary_connect_four_board.x_in_a_row = 4
                temporary_connect_four_board.push(possible_move)
                reward = self.minimax_for_connect_four(self, temporary_connect_four_board, depth_limit - 1, alpha, beta,
                                                       False)[0]
                if reward > maximum_evaluation_value:
                    best_move = possible_move
                    maximum_evaluation_value = reward
                if alpha is not None:
                    alpha = max(alpha, maximum_evaluation_value)
                    if alpha >= beta:
                        break
            return maximum_evaluation_value, best_move
        elif not maximize:
            best_move = None
            minimum_evaluation_value = math.inf
            for possible_move in connect_four_board.possible_moves():
                temporary_connect_four_board = connect_four_board.copy()
                temporary_connect_four_board.x_in_a_row = 4
                temporary_connect_four_board.push(possible_move)
                reward = self.minimax_for_connect_four(self, temporary_connect_four_board, depth_limit - 1, alpha, beta,
                                                       True)[0]
                if reward < minimum_evaluation_value:
                    best_move = possible_move
                    minimum_evaluation_value = reward
                if beta is not None:
                    beta = min(beta, minimum_evaluation_value)
                    if alpha >= beta:
                        break
            return minimum_evaluation_value, best_move

    @staticmethod
    def make_next_connect_four_move(**kwargs):
        self = kwargs.get('self', None)
        board = kwargs.get('board', None)
        _, move = self.minimax_for_connect_four(self, board, 5, self.alpha, self.beta, board.turn == 1)
        return move
