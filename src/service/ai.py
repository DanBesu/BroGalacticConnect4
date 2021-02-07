import copy
import math
import random


EMPTY = 0
PLAYER_PIECE = 1
PC_PIECE = 2
ROWS = 6
COLUMNS = 7
SEQUENCE_LENGTH = 4


class AIBrain:
    """
    Class AIBrain
    ✓ implements the a.i. minimax algorithm for generating an efficient computer move
    ✓ Bibliography
        * https://en.wikipedia.org/wiki/Minimax
        * https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        * https://www.youtube.com/watch?v=y7AKtWGOPAE
        * https://www.youtube.com/watch?v=MMLtza3CZFM&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV&index=6
        * https://www.youtube.com/watch?v=l-hh51ncgDI
    """

    def __init__(self, board):
        self.board = board

    def ai_move(self):
        """
        performs a computer move using the minimax ai algorithm
        :return: winning status (PC_PIECE for win, 0 for ordinary move), the column for the move
        """
        board_copy = copy.deepcopy(self.board)
        col, minimax_score = self.__minimax(board_copy, 5, -math.inf, math.inf, True)

        self.add_piece(board_copy, self.__get_next_empty_row(board_copy, col), col, PC_PIECE)

        if self.wining_move(board_copy, PC_PIECE):
            return PC_PIECE, col
        return 0, col

    @staticmethod
    def add_piece(current_board, row, column, player):
        current_board[row][column] = player

    @staticmethod
    def is_valid_location(current_board, col):
        """
        checks if the column is not full
        :return: boolean value
        """
        return current_board[1][col] == EMPTY

    @staticmethod
    def __get_next_empty_row(current_board, col):
        """
        finds the first empty space in the row
        :return: the index of the row (integer)
        """
        # print('col: ', col)
        for r in range(ROWS, 0, -1):
            if current_board[r][col] == 0:
                return r
        # print('here')

    def __get_valid_locations(self, current_board):
        """
        :return: a list of the current valid locations
        """
        valid_locations = []
        for col in range(1, COLUMNS + 1):
            if self.is_valid_location(current_board, col):
                valid_locations.append(col)
        return valid_locations

    @staticmethod
    def wining_move(current_board, player):
        """
        checks if the current current_board has any winning move
        :param current_board: the current matrix in board format
        :param player: int ( 1 or 2 )
        :return: boolean value
        """

        # check vertical locations for win
        for c in range(1, COLUMNS + 1):
            for r in range(1, ROWS - 2):

                if current_board[r][c] == player and current_board[r + 1][c] == player and current_board[r + 2][
                    c] == player and \
                        current_board[r + 3][c] == player:
                    return True

        # check horizontal locations for win
        for c in range(1, COLUMNS - 2):
            for r in range(1, ROWS + 1):

                if current_board[r][c] == player and current_board[r][c + 1] == player and current_board[r][
                    c + 2] == player and \
                        current_board[r][c + 3] == player:
                    return True

        # check principal diagonals
        for c in range(1, COLUMNS - 2):
            # print('col: ', c)
            for r in range(1, ROWS - 2):
                # print('row: ', r)

                if current_board[r][c] == player and current_board[r + 1][c + 1] == player and current_board[r + 2][
                    c + 2] == player and \
                        current_board[r + 3][c + 3] == player:
                    return True
        # check secondary diagonals
        for c in range(1, COLUMNS - 2):
            for r in range(4, ROWS+1):
                if current_board[r][c] == player and current_board[r - 1][c + 1] == player and current_board[r - 2][
                    c + 2] == player and \
                        current_board[r - 3][c + 3] == player:
                    return True
        return False

    def __is_terminal_node(self, current_board):
        """
        someone winning / all pieces used
        :return: boolean value
        """
        return self.wining_move(current_board, PLAYER_PIECE) or self.wining_move(current_board, PC_PIECE) or len(
            self.__get_valid_locations(current_board)) == 0

    @staticmethod
    def __evaluate_sequence(sequence, player):
        """
        gives a score for a type of move: 4 in a row / 3 in a row / 2 in a row / 3 in a row for the opponent
        :param sequence: list
        :param player: PLAYER / PC
        :return:
        """
        score = 0
        other_piece = PLAYER_PIECE
        if player == PLAYER_PIECE:
            other_piece = PC_PIECE

        if sequence.count(player) == SEQUENCE_LENGTH:  # just if the depth is 0
            score += 100
        elif sequence.count(player) == 3 and sequence.count(EMPTY) == 1:
            score += 5
        elif sequence.count(player) == 2 and sequence.count(EMPTY) == 2:
            score += 2

        if sequence.count(other_piece) == 3 and sequence.count(EMPTY) == 1:
            score -= 4

        return score

    def __score_position(self, current_board, player):
        """
        the score for a current current_board
        :param current_board: the current matrix in board format
        :param player: PLAYER_PIECE / PC_PIECE
        :return: the score for a current current_board (int)
        """
        # look at the whole current_board for the number of 2/3/4-in-a-rows
        score = 0

        # score center column
        center_array = [row[COLUMNS // 2 + 1] for row in current_board[1:-1]]
        center_count = center_array.count(player)
        score += center_count * 3

        # Score Horizontal
        for row in range(1, ROWS + 1):
            row_array = current_board[row][1:-1]
            for col in range(COLUMNS - 3):
                sequence = row_array[col:col + SEQUENCE_LENGTH]
                score += self.__evaluate_sequence(sequence, player)

        # Score Vertical
        for col in range(1, COLUMNS + 1):
            col_array = [row[col] for row in current_board[1:-1]]
            for row in range(ROWS - 3):
                sequence = col_array[row:row + SEQUENCE_LENGTH]
                score += self.__evaluate_sequence(sequence, player)

        # score principal diagonals
        for row in range(1, ROWS - 2):
            for col in range(1, COLUMNS - 2):
                sequence = [current_board[row + i][col + i] for i in range(SEQUENCE_LENGTH)]
                score += self.__evaluate_sequence(sequence, player)

        # score secondary diagonal
        for row in range(1, ROWS - 2):
            for col in range(1, COLUMNS - 2):
                sequence = [current_board[row + 3 - i][col + i] for i in range(SEQUENCE_LENGTH)]
                score += self.__evaluate_sequence(sequence, player)

        return score

    def __minimax(self, current_board, depth, alpha, beta, maximising_player):
        """
        Minimax algorithm for the ai version of computer move
        - the choosing process is based on the score of each possible future board, from the current moment
        - uses alpha/beta pruning for efficiency
        :param current_board: the current matrix in board format
        :param alpha: best score tracker for computer
        :param beta: best score tracker for the player
        :param depth: int
        :param maximising_player: boolean value: TRUE - maximising player, FALSE - minimising player
        :return the column generated by the ai, the score of the column
        """
        valid_locations = self.__get_valid_locations(current_board)
        is_terminal = self.__is_terminal_node(current_board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.wining_move(current_board, PC_PIECE):
                    return None, 1000000000000
                elif self.wining_move(current_board, PLAYER_PIECE):
                    return None, -100000000000
                else:  # game is over, no more valid moves
                    return None, 0
            else:  # depth is zero, so it finds the static evaluation of the current_board
                return None, self.__score_position(current_board, PC_PIECE)

        if maximising_player:
            score_value = -math.inf
            column = random.choice(valid_locations)

            for col in valid_locations:
                row = self.__get_next_empty_row(current_board, col)  # try every empty position,

                board_copy = copy.deepcopy(current_board)  # using a copy of the current_board
                self.add_piece(board_copy, row, col, PC_PIECE)

                max_evaluation = self.__minimax(board_copy, depth - 1, alpha, beta, False)[1]  # get the score of a new deeper current_board
                if max_evaluation > score_value:
                    score_value = max_evaluation
                    column = col
                alpha = max(alpha, score_value)
                if alpha >= beta:
                    break
            return column, score_value

        else:  # minimizing player
            score_value = math.inf
            column = random.choice(valid_locations)

            for col in valid_locations:
                row = self.__get_next_empty_row(current_board, col)
                board_copy = copy.deepcopy(current_board)
                self.add_piece(board_copy, row, col, PLAYER_PIECE)

                max_evaluation = self.__minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if max_evaluation < score_value:
                    score_value = max_evaluation
                    column = col
                beta = min(beta, score_value)
                if alpha >= beta:
                    break
            return column, score_value
