import copy
import unittest

from src.domain.board import Board, MoveError

from src.service.game_service import GameService


class ServiceUnitTest(unittest.TestCase):

    def setUp(self):
        self._board = Board()
        self._service = GameService(self._board)

    def test_pieces(self):
        self.assertEqual(self._service.board.game_pieces, {'player1': 'boss', 'player2': '-'})

    def test_player_move(self):
        self._service.player_move(1)
        self.assertEqual(self._board.data[6][1], 1)

    def test_fighters(self):
        self._service.change_fighters('+', '-')

    def test_player_winning_move(self):
        self._service.reset()
        self._service.board.data[6][1] = 1
        self._service.board.data[6][2] = 1
        self._service.board.data[6][3] = 1
        self._service.board.data[6][4] = 1

        self.assertEqual(self._service.check_win(6, 3, 1, 4), True)
        self.assertEqual(self._service.check_win(3, 4, 1, 4), False)

        self._service.reset()
        self._service.board.data[6][1] = 1
        self._service.board.data[5][1] = 1
        self._service.board.data[4][1] = 1
        self._service.board.data[3][1] = 1

        self.assertEqual(self._service.check_win(5, 1, 1, 4), True)

        self._service.reset()
        self._service.board.data[6][1] = 1
        self._service.board.data[5][2] = 1
        self._service.board.data[4][3] = 1
        self._service.board.data[3][4] = 1

        self.assertEqual(self._service.check_win(5, 2, 1, 4), True)

        self._service.reset()
        self._service.board.data[3][1] = 1
        self._service.board.data[4][2] = 1
        self._service.board.data[5][3] = 1
        self._service.board.data[6][4] = 1

        self.assertEqual(self._service.check_win(4, 2, 1, 4), True)

    def test_difficulty(self):
        self._service.difficulty = 1
        self.assertEqual(self._service.difficulty, 1)

        self._service.difficulty = 4
        self.assertEqual(self._service.difficulty, 4)

    def test_computer_move(self):

        self._service.board.reset()
        b = copy.deepcopy(self._service.board)

        self._service.difficulty = 4
        self._service.computer_move()
        self.assertNotEqual(self._service.board, b)

        # check for win
        self._service.reset()
        self._service.difficulty = 3
        self._service.board.data[6][2] = 2
        self._service.board.data[6][3] = 2
        self._service.board.data[6][4] = 2
        self._service.computer_move()
        self.assertEqual(self._service.board.data[6][1], 2)

        # check for three in a row
        self._service.reset()
        self._service.difficulty = 3
        self._service.board.data[6][2] = 2
        self._service.board.data[6][3] = 2
        self._service.computer_move()
        self.assertEqual(self._service.board.data[6][1], 2)

        # check for two in a row
        self._service.reset()
        self._service.difficulty = 3
        self._service.board.data[6][2] = 2
        self._service.computer_move()
        self.assertEqual(self._service.board.data[6][1], 2)

        for index in range(1, 8):
            self._service.board.data[5][index] = 1
            self._service.board.data[6][index] = 1

        self._service.computer_move()

        self._service.reset()
        self._service.board.data[6][1] = 1
        self._service.board.data[6][4] = 1
        self._service.board.data[5][3] = 1
        self._service.board.data[4][2] = 1

        self._service.computer_move()
        print(self._service.board)

        self._service.reset()
        self._service.difficulty = 1
        self._service.computer_move()
