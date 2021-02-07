"""
- Game Service
    * method: make a move
        params: index of column
    * method: check if it is a winning move (Horizontally, Vertically, Diagonally)
        params: the coordinates of the cell

"""
import random

from src.domain.board import Board, Move, MoveError
from src.service.ai import AIBrain


class GameService:

    def __init__(self, board):
        self._board = board
        self._available_moves = {1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6}
        self._difficulty = 4

    @property
    def board(self):
        return self._board

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

    def reset(self):
        self._board.reset()
        self._available_moves = {1: 6, 2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6}

    def change_fighters(self, player1, player2):
        self._board.game_pieces = {'player1': player1, 'player2': player2}

    def __check_available_moves(self):
        """
        checks if the current_board is full
        :return:
        """
        for available_move in self._available_moves:
            if self._available_moves[available_move] != 0:
                return True
        return False

    def __add_move(self, column, player):
        """
        ✓ creates a Move entity for validation
        ✓ passes the move values to the Board entity
        ✓ updates the dict of available moves
        :param column: int
        :param player: int (1 or 2)
        :return: -
        """
        move = Move(self._board, column, player)
        move.row = self._available_moves[move.column]
        self._available_moves[column] -= 1
        self._board.add_move(move.row, move.column, move.player)

        if not self.__check_available_moves():
            raise MoveError("Wow! Rough game! That is equality.")

    def player_move(self, column):
        self.__add_move(column, 1)
        if self.check_win(self._available_moves[column] + 1, column, 1, 4) is True:
            return 1
        return 0

    def computer_move(self):
        """
        Order of strategic moves:
        1. blocks the player's next winning move by checking all the available moves
        2. tries to find beneficial move for his winning purpose and than check if it helps the player afterwards
        3. random, but check if the move helps the player afterwards
        :return: - winning status - 0 no winner after this move, 1 - player wins, 2 - computer wins
        """

        if self._difficulty == 4:
            ai = AIBrain(self._board.data)
            status, col = ai.ai_move()
            self.__add_move(col, 2)
            return status, col

        if self._difficulty > 1:
            # 1. blocks the player
            for col in self._available_moves:
                if self._available_moves[col] > 0:
                    if self.check_win(self._available_moves[col], col, 1, 4):
                        self.__add_move(col, 2)
                        if self.check_win(self._available_moves[col] + 1, col, 2, 4):
                            return 2, col
                        return 0, col

            # 2. checks for 4, for 3 and for 2 in his advantage, but also checks for the next above move not to be in the player's advantage (if dif = 3)
            for col in self._available_moves:
                row = self._available_moves[col]
                if row > 0:
                    if self.check_win(row, col, 2, 4):
                        self.__add_move(col, 2)
                        return 2, col

                    if self.check_win(row, col, 2, 3):
                        if self._difficulty == 3 and row > 1 and self.check_win(row - 1, col, 1, 4) is False:
                            self.__add_move(col, 2)
                            return 0, col
                        elif self._difficulty < 3:
                            self.__add_move(col, 2)
                            return 0, col

                    if self.check_win(row, col, 2, 2):
                        if self._difficulty == 3 and row > 1 and self.check_win(row - 1, col, 1, 4) is False:
                            self.__add_move(col, 2)
                            return 0, col
                        elif self._difficulty < 3:
                            self.__add_move(col, 2)
                            return 0, col

        # 3. tries a random value, but checks for the next above move not to be in the player's advantage (if dif = 3)
        available_list = []
        for col in self._available_moves:
            if self._available_moves[col] > 0:
                available_list.append(col)

        if self._difficulty == 3:
            for col in self._available_moves:
                if self._available_moves[col] > 0:
                    if self.check_win(self._available_moves[col], col, 1, 4) is False:
                        self.__add_move(col, 2)
                        if self.check_win(self._available_moves[col] + 1, col, 2, 4):
                            return 2, col
                        return 0, col

        col_ = random.choice(available_list)
        self.__add_move(col_, 2)
        if self.check_win(self._available_moves[col_] + 1, col_, 2, 4):
            return 2, col_
        return 0, col_

    def check_win(self, row, column, player, how_many):
        """
        ✓ checks if the current move is a winning one
        :return: boolean value corresponding with the winning status
        """
        # horizontally right
        count = 1
        i = row
        j = column + 1
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            j += 1
            current_player_value = self._board.data[i][j]

        # horizontally left // continue with the current counter
        i = row
        j = column - 1
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            j -= 1
            current_player_value = self._board.data[i][j]

        # vertically up
        count = 1
        i = row - 1
        j = column
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            i -= 1
            current_player_value = self._board.data[i][j]

        # vertically down // continue with the current counter
        i = row + 1
        j = column
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            i += 1
            current_player_value = self._board.data[i][j]

        # principal diagonal down
        count = 1
        i = row - 1
        j = column - 1
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            i -= 1
            j -= 1
            current_player_value = self._board.data[i][j]

        # principal diagonal up // continue with the current counter
        i = row + 1
        j = column + 1
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            i += 1
            j += 1
            current_player_value = self._board.data[i][j]

        # secondary diagonal down /
        count = 1
        i = row + 1
        j = column - 1
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            i += 1
            j -= 1
            current_player_value = self._board.data[i][j]

        # secondary diagonal up // continue with the current counter
        i = row - 1
        j = column + 1
        current_player_value = self._board.data[i][j]

        while current_player_value == player:
            count += 1
            if count == how_many:
                return True
            i -= 1
            j += 1
            current_player_value = self._board.data[i][j]

        # we like it raw, no functions 💪😎
        return False
