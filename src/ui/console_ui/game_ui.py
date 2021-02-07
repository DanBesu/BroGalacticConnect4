import sys

from src.service.game_service import GameService, MoveError


class MainMenuUI:

    @staticmethod
    def display():
        print('0. exit')
        print('1. Start')
        print('2. Settings')

    @staticmethod
    def exit():
        print('Bye bye')
        sys.exit(0)


class GameUI:

    def __init__(self, game_service):
        self._game_service = game_service

    def display_board(self):
        print(self._game_service.board)

    def move_ui(self, player):
        column_dict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
        if player == 1:

            column = input("your column: ")
            column = column.upper()

            if column in column_dict:
                column = column_dict[column]
            else:
                raise MoveError('please input a valid column')

            winning_status = self._game_service.player_move(column)
            if winning_status:
                self.end_game(winning_status)
                return True
            else:
                return False
        elif player == 2:
            winning_status, col = self._game_service.computer_move()
            if winning_status:
                self.end_game(winning_status)
                return True
            else:
                return False

    def end_game(self, winner):
        print(str(self._game_service.board))
        self._game_service.reset()
        if winner == 1:
            print('You won!')
        elif winner == 2:
            print('Loser!')


class SettingsUI:

    def __init__(self, game_service):
        self._game_service = game_service

    @staticmethod
    def display():
        print('0. go back')
        print('1. Personalise your game!')
        print('2. Choose your game mode!')

    @staticmethod
    def back_command():
        print('See u on the field!')

    def input_players(self):

        print('You have to choose some characters for you and for the computer!')
        player1 = input('Chose your fighter: ').strip()
        player2 = input('Your opponent: ').strip()
        if player1 in ['\n', '', ' '] or player2 in ['\n', '', ' ']:
            raise SettingsInputError('you should use visible characters')
        self._game_service.change_fighters(player1, player2)

    def input_difficulty(self):
        difficulty_dict = {'babycandy': 1, 'casual': 2, 'insane': 3, 'warzone': 4}
        print('Chose the difficulty by your IQ level: ')

        for d in difficulty_dict:
            print(d)

        difficulty = input('... ').lower().strip()
        if difficulty in difficulty_dict:
            self._game_service.difficulty = difficulty_dict[difficulty]
        else:
            raise SettingsInputError('invalid difficulty, please chose from the menu')


class SettingsInputError(Exception):
    def __init__(self, message):
        self._message = message
