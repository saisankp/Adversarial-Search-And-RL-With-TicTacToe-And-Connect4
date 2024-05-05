import io
import math
import sys
import matplotlib.pyplot as plt
import inquirer
from pyfiglet import figlet_format
from tqdm import tqdm

from games.connect_four import ConnectFour
from games.tic_tac_toe import TicTacToe
from opponents.default_opponent import DefaultOpponent
from opponents.human_opponent import HumanOpponent
from opponents.minimax_opponent import MinimaxOpponent
from opponents.tabular_q_learning_opponent import TabularQLearningOpponent

# Print welcome banner!
print(
    figlet_format("Welcome to Prathamesh's Minimax and RL algorithm explorer for CS7IS2!", justify='center', width=140))

# Either run an individual algorithm or compare multiple algorithms
answer = inquirer.prompt([inquirer.List("wish", message="I want to", choices=["Train a q-agent",
                                                                              "Run a game manually",
                                                                              "Compare algorithms", "Exit"])])
# Train a q-agent
if answer["wish"] == "Train a q-agent":
    answer = inquirer.prompt(
        [inquirer.List("train", message="I want to train for", choices=["Tic Tac Toe", "Connect four"])])
    train = inquirer.prompt([inquirer.Text("rounds", message="How many rounds do you want to train for?",
                                           validate=lambda _, c: c.isdigit() and int(c) > 0)])
    name = inquirer.prompt([inquirer.Text("file", message="What name do you want for the resulting pickle file?",
                                          validate=lambda _, c: isinstance(c, str))])
    # Training q-agent for Tic Tac Toe
    if answer['train'] == "Tic Tac Toe":
        p1 = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
        p2 = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
        game = TicTacToe(p1, p2)
        game.train(int(train['rounds']))
        p1.save_policy(f"{name['file']}-1")
        p2.save_policy(f"{name['file']}-2")
    # Training q-agent for Connect Four
    elif answer['train'] == "Connect four":
        p1 = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
        p2 = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
        game = ConnectFour(p1, p2)
        game.train(int(train['rounds']))
        p1.save_policy(f"{name['file']}-1")
        p2.save_policy(f"{name['file']}-2")

# Run a game manually
elif answer["wish"] == "Run a game manually":
    answer = inquirer.prompt([inquirer.List("game", message="Which game do you want to play?",
                                            choices=["Tic Tac Toe", "Connect four", "Exit"])])
    if answer["game"] == "Tic Tac Toe":
        answer = inquirer.prompt([inquirer.List("opponent_one", message="Who is opponent one?",
                                                choices=["Human", "Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])
        # Set first player
        if answer["opponent_one"] == "Human":
            first_player = HumanOpponent()
        elif answer["opponent_one"] == "Default":
            first_player = DefaultOpponent()
        elif answer["opponent_one"] == "Minimax (with alpha-beta pruning)":
            first_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_one"] == "Minimax (without alpha-beta pruning)":
            first_player = MinimaxOpponent(None, None)
        else:
            first_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            first_player.load_policy()

        answer = inquirer.prompt([inquirer.List("opponent_two", message="Who is opponent two?",
                                                choices=["Human", "Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])

        # Set second player
        if answer["opponent_two"] == "Human":
            second_player = HumanOpponent()
        elif answer["opponent_two"] == "Default":
            second_player = DefaultOpponent()
        elif answer["opponent_two"] == "Minimax (with alpha-beta pruning)":
            second_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_two"] == "Minimax (without alpha-beta pruning)":
            second_player = MinimaxOpponent(None, None)
        else:
            second_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            second_player.load_policy()

        game = TicTacToe(first_player, second_player)
        game.play()
        sys.exit()

    if answer["game"] == "Connect four":
        answer = inquirer.prompt([inquirer.List("opponent_one", message="Who is opponent one?",
                                                choices=["Human", "Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])
        # Set first player
        if answer["opponent_one"] == "Human":
            first_player = HumanOpponent()
        elif answer["opponent_one"] == "Default":
            first_player = DefaultOpponent()
        elif answer["opponent_one"] == "Minimax (with alpha-beta pruning)":
            first_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_one"] == "Minimax (without alpha-beta pruning)":
            first_player = MinimaxOpponent(None, None)
        else:
            first_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            first_player.load_policy()

        answer = inquirer.prompt([inquirer.List("opponent_two", message="Who is opponent two?",
                                                choices=["Human", "Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])

        # Set second player
        if answer["opponent_two"] == "Human":
            second_player = HumanOpponent()
        elif answer["opponent_two"] == "Default":
            second_player = DefaultOpponent()
        elif answer["opponent_two"] == "Minimax (with alpha-beta pruning)":
            second_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_two"] == "Minimax (without alpha-beta pruning)":
            second_player = MinimaxOpponent(None, None)
        else:
            second_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            second_player.load_policy()

        game = ConnectFour(first_player, second_player)
        game.play()
        sys.exit()

# Compare algorithms
elif answer["wish"] == "Compare algorithms":
    answer = inquirer.prompt([inquirer.List("game", message="Which game do you want to compare with?",
                                            choices=["Tic Tac Toe", "Connect four", "Exit"])])

    iterations = inquirer.prompt(
        [inquirer.Text("number of rounds", message="Which many times do you want to run the game?",
                       validate=lambda _, c: c.isdigit() and int(c) > 1)])
    if answer["game"] == "Tic Tac Toe":
        answer = inquirer.prompt([inquirer.List("opponent_one", message="Who is opponent one?",
                                                choices=["Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])
        if answer["opponent_one"] == "Default":
            first_player = DefaultOpponent()
        elif answer["opponent_one"] == "Minimax (with alpha-beta pruning)":
            first_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_one"] == "Minimax (without alpha-beta pruning)":
            first_player = MinimaxOpponent(None, None)
        else:
            first_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            first_player.load_policy()

        answer = inquirer.prompt([inquirer.List("opponent_two", message="Who is opponent two?",
                                                choices=["Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])
        if answer["opponent_two"] == "Default":
            second_player = DefaultOpponent()
        elif answer["opponent_two"] == "Minimax (with alpha-beta pruning)":
            second_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_two"] == "Minimax (without alpha-beta pruning)":
            second_player = MinimaxOpponent(None, None)
        else:
            second_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            second_player.load_policy()

        ties = 0
        first_player_wins = 0
        second_player_wins = 0
        first_player_time_taken = 0
        second_player_time_taken = 0
        first_player_time_taken_one_round = 0
        second_player_time_taken_one_round = 0
        first_player_max_memory = 0
        second_player_max_memory = 0
        first_player_max_memory_one_round = 0
        second_player_max_memory_one_round = 0
        progress_bar = tqdm(total=int(iterations['number of rounds']))

        for i in range(int(int(iterations['number of rounds'])/2)):
            game = TicTacToe(first_player, second_player)
            text_trap = io.StringIO()
            sys.stdout = text_trap
            result, first_player_time_taken_one_round, second_player_time_taken_one_round, first_player_max_memory_one_round, second_player_max_memory_one_round = game.play()
            sys.stdout = sys.__stdout__
            first_player_time_taken = first_player_time_taken + first_player_time_taken_one_round
            second_player_time_taken = second_player_time_taken + second_player_time_taken_one_round
            first_player_max_memory = first_player_max_memory + first_player_max_memory_one_round
            second_player_max_memory = second_player_max_memory + second_player_max_memory_one_round
            progress_bar.update(1)
            if result == 0:
                ties = ties + 1
            elif result == 1:
                first_player_wins = first_player_wins + 1
            elif result == 2:
                second_player_wins = second_player_wins + 1

        for i in range(int(int(iterations['number of rounds'])/2)):
            game = TicTacToe(second_player, first_player)
            text_trap = io.StringIO()
            sys.stdout = text_trap
            result, second_player_time_taken_one_round, first_player_time_taken_one_round, second_player_max_memory_one_round, first_player_max_memory_one_round = game.play()
            sys.stdout = sys.__stdout__
            first_player_time_taken = first_player_time_taken + first_player_time_taken_one_round
            second_player_time_taken = second_player_time_taken + second_player_time_taken_one_round
            first_player_max_memory = first_player_max_memory + first_player_max_memory_one_round
            second_player_max_memory = second_player_max_memory + second_player_max_memory_one_round
            progress_bar.update(1)
            if result == 0:
                ties = ties + 1
            elif result == 1:
                second_player_wins = second_player_wins + 1
            elif result == 2:
                first_player_wins = first_player_wins + 1

        average_first_player_time_taken = first_player_time_taken / int(iterations['number of rounds'])
        average_second_player_time_taken = second_player_time_taken / int(iterations['number of rounds'])
        average_first_player_max_memory = first_player_max_memory / int(iterations['number of rounds'])
        average_second_player_max_memory = second_player_max_memory / int(iterations['number of rounds'])
        print(f'Number of ties: {ties} ties')
        print(f'First player number of wins: {first_player_wins} wins')
        print(f'First player average time taken: {average_first_player_time_taken} seconds')
        print(f'First player average max memory: {average_first_player_max_memory} bytes')
        print(f'Second player number of wins: {second_player_wins} wins')
        print(f'Second player average time taken: {average_second_player_time_taken} seconds')
        print(f'Second player average max memory: {average_second_player_max_memory} bytes')

        data = {f'{first_player.__class__.__name__}-Player1': first_player_wins,
                f'{second_player.__class__.__name__}-Player2': second_player_wins,
                f'Ties': ties}
        players = list(data.keys())
        wins = list(data.values())
        fig = plt.figure(figsize=(10, 5))
        plt.bar(players, wins, color='green', width=0.4)
        plt.xlabel("Game results")
        plt.ylabel("Rounds")
        plt.title(f"Tic Tac Toe: {first_player.__class__.__name__}-Player1 vs {second_player.__class__.__name__}-Player2 for {iterations['number of rounds']} rounds")
        plt.show()
        sys.exit()

    if answer["game"] == "Connect four":
        answer = inquirer.prompt([inquirer.List("opponent_one", message="Who is opponent one?",
                                                choices=["Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])
        if answer["opponent_one"] == "Default":
            first_player = DefaultOpponent()
        elif answer["opponent_one"] == "Minimax (with alpha-beta pruning)":
            first_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_one"] == "Minimax (without alpha-beta pruning)":
            first_player = MinimaxOpponent(None, None)
        else:
            first_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            first_player.load_policy()

        answer = inquirer.prompt([inquirer.List("opponent_two", message="Who is opponent two?",
                                                choices=["Default", "Minimax (with alpha-beta pruning)",
                                                         "Minimax (without alpha-beta pruning)",
                                                         "Tabular Q-Learning"])])
        if answer["opponent_two"] == "Default":
            second_player = DefaultOpponent()
        elif answer["opponent_two"] == "Minimax (with alpha-beta pruning)":
            second_player = MinimaxOpponent(-math.inf, math.inf)
        elif answer["opponent_two"] == "Minimax (without alpha-beta pruning)":
            second_player = MinimaxOpponent(None, None)
        else:
            second_player = TabularQLearningOpponent(alpha=0.1, epsilon=0.9, gamma=0.9)
            second_player.load_policy()

        ties = 0
        first_player_wins = 0
        second_player_wins = 0
        first_player_time_taken = 0
        second_player_time_taken = 0
        first_player_time_taken_one_round = 0
        second_player_time_taken_one_round = 0
        first_player_max_memory = 0
        second_player_max_memory = 0
        first_player_max_memory_one_round = 0
        second_player_max_memory_one_round = 0
        progress_bar = tqdm(total=int(iterations['number of rounds']))

        for i in range(int(int(iterations['number of rounds']) / 2)):
            game = ConnectFour(first_player, second_player)
            text_trap = io.StringIO()
            sys.stdout = text_trap
            result, first_player_time_taken_one_round, second_player_time_taken_one_round, first_player_max_memory_one_round, second_player_max_memory_one_round = game.play()
            sys.stdout = sys.__stdout__
            first_player_time_taken = first_player_time_taken + first_player_time_taken_one_round
            second_player_time_taken = second_player_time_taken + second_player_time_taken_one_round
            first_player_max_memory = first_player_max_memory + first_player_max_memory_one_round
            second_player_max_memory = second_player_max_memory + second_player_max_memory_one_round
            progress_bar.update(1)
            if result == 0:
                ties = ties + 1
            elif result == 1:
                first_player_wins = first_player_wins + 1
            elif result == 2:
                second_player_wins = second_player_wins + 1

        for i in range(int(int(iterations['number of rounds']) / 2)):
            game = ConnectFour(second_player, first_player)
            text_trap = io.StringIO()
            sys.stdout = text_trap
            result, second_player_time_taken_one_round, first_player_time_taken_one_round, second_player_max_memory_one_round, first_player_max_memory_one_round = game.play()
            sys.stdout = sys.__stdout__
            first_player_time_taken = first_player_time_taken + first_player_time_taken_one_round
            second_player_time_taken = second_player_time_taken + second_player_time_taken_one_round
            first_player_max_memory = first_player_max_memory + first_player_max_memory_one_round
            second_player_max_memory = second_player_max_memory + second_player_max_memory_one_round
            progress_bar.update(1)
            if result == 0:
                ties = ties + 1
            elif result == 1:
                second_player_wins = second_player_wins + 1
            elif result == 2:
                first_player_wins = first_player_wins + 1

        average_first_player_time_taken = first_player_time_taken / int(iterations['number of rounds'])
        average_second_player_time_taken = second_player_time_taken / int(iterations['number of rounds'])
        average_first_player_max_memory = first_player_max_memory / int(iterations['number of rounds'])
        average_second_player_max_memory = second_player_max_memory / int(iterations['number of rounds'])
        print(f'Number of ties: {ties} ties')
        print(f'First player number of wins: {first_player_wins} wins')
        print(f'First player average time taken: {average_first_player_time_taken} seconds')
        print(f'First player average max memory: {average_first_player_max_memory} bytes')
        print(f'Second player number of wins: {second_player_wins} wins')
        print(f'Second player average time taken: {average_second_player_time_taken} seconds')
        print(f'Second player average max memory: {average_second_player_max_memory} bytes')

        data = {f'{first_player.__class__.__name__}-Player1': first_player_wins,
                f'{second_player.__class__.__name__}-Player2': second_player_wins,
                f'Ties': ties}
        players = list(data.keys())
        wins = list(data.values())
        fig = plt.figure(figsize=(10, 5))
        plt.bar(players, wins, color='green', width=0.4)
        plt.xlabel("Game results")
        plt.ylabel("Rounds")
        plt.title(
            f"Connect 4: {first_player.__class__.__name__}-Player1 vs {second_player.__class__.__name__}-Player2 for {iterations['number of rounds']} rounds")
        plt.show()
        sys.exit()
