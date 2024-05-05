import pickle

import numpy as np


class TabularQLearningOpponent:
    def __init__(self, alpha, epsilon, gamma):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.Q_table = {}
        self.states = []

    def load_policy(self):
        loaded = False
        while not loaded:
            pickle_file_name = input('What is the name of the pickle file from training your q-agent: ')
            try:
                pickle_file = open(pickle_file_name, 'rb')
                self.Q_table = pickle.load(pickle_file)
                pickle_file.close()
                loaded = True
            except FileNotFoundError:
                print(f'Pickle file named {pickle_file_name} not found. Try again')

    def update_states_as_empty(self):
        self.states = []

    def save_policy(self, pickle_file_name):
        pickle_file = open(pickle_file_name, 'wb')
        pickle.dump(self.Q_table, pickle_file)
        pickle_file.close()

    def set_state_of_agent(self, state):
        self.states.append(state)

    def q_learning_update(self, reward):
        for state in reversed(self.states):
            if self.Q_table.get(state) is None:
                self.Q_table[state] = 0
            self.Q_table[state] += self.alpha * (self.gamma * reward - self.Q_table[state])
            reward = self.Q_table[state]

    def update_epsilon(self, episode):
        self.epsilon = max(0.3, self.epsilon - 0.000001 * episode)

    @staticmethod
    def board(tictactoe_or_connect_four_board):
        return str(tictactoe_or_connect_four_board.board.flatten())

    @staticmethod
    def make_next_tic_tac_toe_move(**kwargs):
        move = None
        self = kwargs.get('self', None)
        possible_board_moves = kwargs.get('positions', None)
        board = kwargs.get('board', None)
        if np.random.uniform(0, 1) <= self.epsilon:
            move = possible_board_moves[np.random.choice(len(possible_board_moves))]
        else:
            max_q_value = float('-inf')
            for possible_move in possible_board_moves:
                upcoming_tictoctoe_board = board.copy()
                upcoming_tictoctoe_board.push(tuple(possible_move))
                upcoming_tictoctoe_board_state = self.board(upcoming_tictoctoe_board)
                if self.Q_table.get(upcoming_tictoctoe_board_state) is None:
                    q_value = 0
                else:
                    q_value = self.Q_table.get(upcoming_tictoctoe_board_state)
                if q_value >= max_q_value:
                    max_q_value = q_value
                    move = possible_move
        return move

    @staticmethod
    def make_next_connect_four_move(**kwargs):
        best_move = None
        self = kwargs.get('self', None)
        possible_board_moves = kwargs.get('positions', None)
        board = kwargs.get('board', None)
        if np.random.uniform(0, 1) <= self.epsilon:
            best_move = np.random.choice(board.possible_moves())
        else:
            maximum_q_value = float('-inf')
            for possible_move in possible_board_moves:
                upcoming_connect_four_board = board.copy()
                upcoming_connect_four_board.x_in_a_row = 4
                upcoming_connect_four_board.push(possible_move)
                upcoming_connect_four_board_state = self.board(upcoming_connect_four_board)
                if self.Q_table.get(upcoming_connect_four_board_state) is None:
                    q_value = 0
                else:
                    q_value = self.Q_table.get(upcoming_connect_four_board_state)
                if q_value >= maximum_q_value:
                    maximum_q_value = q_value
                    best_move = possible_move
        return best_move
