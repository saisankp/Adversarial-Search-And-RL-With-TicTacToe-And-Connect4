class HumanOpponent:

    @staticmethod
    def make_next_tic_tac_toe_move(**kwargs):
        possible_board_positions = kwargs.get('positions', None)
        while True:
            board_row = int(input('Next move (row): '))
            board_column = int(input('Next move (column): '))
            possible_move = (board_column, board_row)
            if possible_move in possible_board_positions:
                return possible_move
            else:
                print("That place is outside the board. Try again.")

    @staticmethod
    def make_next_connect_four_move(**kwargs):
        while True:
            board_column = int(input('Enter col: '))
            return board_column
