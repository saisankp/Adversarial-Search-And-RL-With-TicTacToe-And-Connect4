import time
import tracemalloc
from IPython.core.display_functions import clear_output
from tictactoe import Board
from tqdm import tqdm


class ConnectFour:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.board = ConnectFourBoard(dimensions=(6, 7))
        self.board_as_string = None
        self.board.x_in_a_row = 4

    def connect_four_board(self):
        self.board_as_string = str(self.board.board.flatten())
        return self.board_as_string

    def set_learning_reward(self):
        result = self.board.result()
        if result == 1:
            self.first_player.q_learning_update(1)
            self.first_player.q_learning_update(-1)
        if result == 2:
            self.first_player.q_learning_update(1)
            self.first_player.q_learning_update(-1)
        else:
            self.first_player.q_learning_update(0)
            self.first_player.q_learning_update(0)

    def reset_board(self):
        self.board = ConnectFourBoard(dimensions=(6, 7))
        self.board.x_in_a_row = 4
        self.board_as_string = None

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
                move = self.first_player.make_next_connect_four_move(self=self.first_player, positions=positions,
                                                                     board=self.board)
                self.board.push(move)
            except ValueError or IndexError:
                print("That column is filled. Try another column.")
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
                    print(f'{self.first_player.__class__.__name__} has won.')
                else:
                    print("It is a tie.")
                self.reset_board()
                break
            else:
                positions = self.board.possible_moves()
                print(f"{self.second_player.__class__.__name__}'s turn (marking as 0)")
                start_time = time.time()
                tracemalloc.start()
                try:
                    move = self.second_player.make_next_connect_four_move(self=self.second_player, positions=positions,
                                                                          board=self.board)
                    self.board.push(move)
                except ValueError or IndexError:
                    print("That column is filled. Try another column.")
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
                        print(f'{self.second_player.__class__.__name__} has won.')
                    else:
                        print("It is a tie.")
                    self.reset_board()
                    break
        return winner, first_player_time_taken, second_player_time_taken, first_player_max_memory_used, second_player_max_memory_used

    def train(self, iterations):
        for i in tqdm(range(iterations)):
            self.first_player.update_epsilon(i)
            self.second_player.update_epsilon(i)
            while True:
                positions = self.board.possible_moves()
                first_player_action = self.first_player.make_next_connect_four_move(self=self.first_player,
                                                                                    positions=positions,
                                                                                    board=self.board)
                self.board.push(first_player_action)
                board_as_string = self.connect_four_board()
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
                    second_player_action = self.second_player.make_next_connect_four_move(self=self.second_player,
                                                                                          positions=positions,
                                                                                          board=self.board)
                    self.board.push(second_player_action)
                    board_as_string = self.connect_four_board()
                    self.second_player.set_state_of_agent(board_as_string)

                    winner = self.board.result()
                    if winner is not None:
                        self.set_learning_reward()
                        self.first_player.update_states_as_empty()
                        self.second_player.update_states_as_empty()
                        self.reset_board()
                        break


class ConnectFourBoard(Board):
    def __init__(self, dimensions):
        self.state_dict = dict()
        super().__init__(dimensions, x_in_a_row=4)

    def push(self, column):
        for possible_move in super().possible_moves():
            self.state_dict[possible_move[0]] = []
        for possible_move in super().possible_moves():
            self.state_dict[possible_move[0]].append(possible_move[1])
        super().push((column, max(self.state_dict[column])))

    def copy(self):
        board = ConnectFourBoard(self.dimensions)
        board.state_dict = self.state_dict
        board.board = self.board.copy()
        board.turn = self.turn
        return board

    def possible_moves(self):
        possible_moves_list = []
        for possible_move in super().possible_moves():
            if possible_move[0] not in possible_moves_list:
                possible_moves_list.append(possible_move[0])
        return possible_moves_list
