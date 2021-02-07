"""
- Board Class:
    * field: pieces introduced by the user
    * field: 15 x 15 matrix - cell: 0 (empty) / 1 (p1) / 2 (p2)
    * getters / setters
    * method: str - ui version
"""
from texttable import Texttable


class Board:

    def __init__(self):
        """
        pieces: dict { player1, player2 }
        """

        self.ROWS = 6
        self.COLUMNS = 7
        self.PLAYER = 1
        self.PC = 2
        self._game_pieces = {'player1': 'boss', 'player2': '-'}
        self._data = [[0 for col in range(self.COLUMNS + 2)] for row in range(self.ROWS + 2)]

        # border the current_board with -1's
        for index in range(self.ROWS + 2):
            self._data[index][0] = -1
        for index in range(self.COLUMNS + 2):
            self._data[0][index] = -1
        for index in range(self.ROWS + 2):
            self._data[index][self.COLUMNS + 1] = -1
        for index in range(self.COLUMNS + 2):
            self._data[self.ROWS + 1][index] = -1

    @property
    def data(self):
        return self._data

    @property
    def game_pieces(self):
        return self._game_pieces

    @game_pieces.setter
    def game_pieces(self, value):
        self._game_pieces = value

    def add_move(self, row, column, player):
        """
        sets a new move to the current_board
        """
        self._data[row][column] = player

    def reset(self):
        self._data = [[0 for col in range(self.COLUMNS + 2)] for row in range(self.ROWS + 2)]
        # border the current_board with -1's
        for index in range(self.ROWS + 2):
            self._data[index][0] = -1
        for index in range(self.COLUMNS + 2):
            self._data[0][index] = -1
        for index in range(self.ROWS + 2):
            self._data[index][self.COLUMNS + 1] = -1
        for index in range(self.COLUMNS + 2):
            self._data[self.ROWS + 1][index] = -1

    def __str__(self):
        table = Texttable()

        # add each table row
        for row in range(1, self.ROWS + 1):
            data_ = []
            for column in range(1, self.COLUMNS + 1):
                if self._data[row][column] == 0:
                    data_.append(' ')
                if self._data[row][column] == self.PLAYER:
                    data_.append(self._game_pieces['player1'])
                if self._data[row][column] == self.PC:
                    data_.append(self._game_pieces['player2'])
            beautiful_row_index = '.' + str(row) + '.'
            table.add_row([beautiful_row_index] + data_ + [beautiful_row_index])

        # add footer
        footer = []
        for index in range(self.COLUMNS):
            footer.append(str(chr(index + 65)))
        table.add_row([' '] + footer + [' '])

        return table.draw()


class Move:
    def __init__(self, board, column, player):
        """
        ✓ keeps the required data for a certain move
        ✓ validates the data
        ✓ finds the row

        :param board: Board entity
        :param column: int
        :param player: int ( 1 / 2 )
        """
        self._board = board
        self.column = column
        self.player = player
        self.row = None

        if self.column > self._board.COLUMNS or self.column < 1:
            raise MoveError('column out of bounds')

        if self._board.data[1][column] != 0:
            raise MoveError('this column is full, try another one')


class MoveError(Exception):
    def __init__(self, message):
        self._message = message
