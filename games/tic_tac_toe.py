import time
import tracemalloc
from IPython.core.display_functions import clear_output
from tictactoe import Board
from tqdm import tqdm


class TicTacToe:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.board = Board(dimensions=(3, 3))
        self.board_as_string = None

    def tictactoe_board(self):
        self.board_as_string = str(self.board.board.flatten())
        return self.board_as_string

    def reset_board(self):
        self.board = Board()
        self.board_as_string = None

    def set_learning_reward(self):
        result = self.board.result()
        if result == 1:
            self.first_player.q_learning_update(1)
            self.second_player.q_learning_update(-1)
        if result == 2:
            self.first_player.q_learning_update(-1)
            self.second_player.q_learning_update(1)
        else:
            self.first_player.q_learning_update(0)
            self.second_player.q_learning_update(0)

    def play(self):
        winner = None
        first_player_time_taken = 0
        first_player_max_memory_used = 0
        second_player_time_taken = 0
        second_player_max_memory_used = 0
        print(self.board)
        while True:
            positions = self.board.possible_moves()
            print(f"{self.first_player.__class__.__name__}'s turn (marking as X)")
            start_time = time.time()
            tracemalloc.start()
            try:
                first_player_action = self.first_player.make_next_tic_tac_toe_move(self=self.first_player,
                                                                                   positions=positions,
                                                                                   board=self.board)
                self.board.push(first_player_action)
            except (ValueError, IndexError):
                print("That place is taken already or you are out of bounds. Try again.")
                continue
            end_time = time.time()
            first_player_max_memory_used = first_player_max_memory_used + (tracemalloc.get_traced_memory()[1])
            tracemalloc.stop()
            first_player_time_taken = first_player_time_taken + (end_time - start_time)
            clear_output()
            print(self.board)
            winner = self.board.result()
            if winner is not None:
                if winner == 1:
                    print(self.first_player.__class__.__name__, "has won.")
                else:
                    print("tie!")
                self.reset_board()
                break
            else:
                positions = self.board.possible_moves()
                print(f"{self.second_player.__class__.__name__}'s turn (marking as 0)")
                start_time = time.time()
                tracemalloc.start()
                try:
                    second_player_action = self.second_player.make_next_tic_tac_toe_move(self=self.second_player,
                                                                                         positions=positions,
                                                                                         board=self.board)
                    self.board.push(second_player_action)
                except (ValueError, IndexError):
                    print("That place is taken already or you are out of bounds. Try again.")
                    continue
                end_time = time.time()
                second_player_max_memory_used = second_player_max_memory_used + (
                    tracemalloc.get_traced_memory()[1])
                tracemalloc.stop()
                second_player_time_taken = second_player_time_taken + (end_time - start_time)
                clear_output()
                print(self.board)
                winner = self.board.result()
                if winner is not None:
                    if winner == 2:
                        print(self.second_player.__class__.__name__, "has won.")
                    else:
                        print("It is a tie.")
                    self.reset_board()
                    break
        return winner, first_player_time_taken, second_player_time_taken, first_player_max_memory_used, second_player_max_memory_used

    def train(self, rounds):
        for i in tqdm(range(rounds)):
            self.first_player.update_epsilon(i)
            self.second_player.update_epsilon(i)
            while True:
                positions = self.board.possible_moves()
                first_player_action = self.first_player.make_next_tic_tac_toe_move(self=self.first_player,
                                                                                   positions=positions,
                                                                                   board=self.board)
                self.board.push(first_player_action)
                board_as_string = self.tictactoe_board()
                self.first_player.set_state_of_agent(board_as_string)
                winner = self.board.result()
                if winner is not None:
                    self.set_learning_reward()
                    self.first_player.update_states_as_empty()
                    self.second_player.update_states_as_empty()
                    self.reset_board()
                    break
                else:
                    positions = self.board.possible_moves()
                    second_player_action = self.second_player.make_next_tic_tac_toe_move(self=self.second_player,
                                                                                         positions=positions,
                                                                                         board=self.board)
                    self.board.push(second_player_action)
                    board_as_string = self.tictactoe_board()
                    self.second_player.set_state_of_agent(board_as_string)
                    winner = self.board.result()
                    if winner is not None:
                        self.set_learning_reward()
                        self.first_player.update_states_as_empty()
                        self.second_player.update_states_as_empty()
                        self.reset_board()
                        break
