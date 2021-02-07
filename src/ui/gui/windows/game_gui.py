import sys

import pygame

from src.domain.board import MoveError

PLAYER_TURN = 0
COMPUTER_TURN = 1

ROWS = 6
COLUMNS = 7
SEQUENCE_LENGTH = 4
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 10)

width = COLUMNS * SQUARE_SIZE
height = (ROWS + 2) * SQUARE_SIZE
screen_size = (width, height)

pygame.init()


class TransitionToGame:
    """
    makes the transition between the menu and the game with an image
    """
    @staticmethod
    def show(transition_image):
        screen = pygame.display.set_mode(screen_size)
        screen.blit(transition_image, (0, 0))
        pygame.display.update()

        clock = pygame.time.Clock()
        start = 1
        while start < 100:
            start += 1
            clock.tick(20)


class GameWindow:

    def __init__(self, service, theme):
        self._service = service
        self._board = service.board
        self._theme = theme
        self._screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('BroGalactic Connect4')

    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        self._theme = value

    def render_game(self):

        self._screen.blit(self._theme.background, (0, 0))
        self._draw_board(self._board)
        pygame.display.update()

        turn = 0
        game_over = False
        go_back = False

        clock = pygame.time.Clock()

        while not game_over and not go_back:
            self._draw_board(self._board)

            # goes back to the main menu if quit button pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    go_back = True

                # controls the player icon left and right
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    if turn == 0:
                        self._screen.blit(self._theme.background, (0, 0))
                        self._screen.blit(self._theme.player_image, (posx - 30, 110))
                        self._draw_board(self._board)
                        pygame.display.update()

                # executes a player move when mouse pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if turn == PLAYER_TURN:
                        animation_index = 110

                        x = event.pos[0]
                        column = int(x // SQUARE_SIZE) + 1

                        # drop the animation
                        while animation_index < height:
                            self._screen.blit(self._theme.background, (0, 0))
                            animation_index += 1
                            self._screen.blit(self._theme.player_image, (x - 27, animation_index))

                            pygame.display.update()
                            clock.tick(500)
                        try:
                            winning_status = self._service.player_move(column)
                            if winning_status == 1:

                                # print wining labels
                                label = self._theme.font.render("GOOD JOB!", 1, (255, 255, 0))
                                self._screen.blit(label, (250, 10))

                                # update the board
                                self._draw_board(self._board)
                                self._service.reset()
                                game_over = True

                            turn += 1
                            turn = turn % 2
                            self._draw_board(self._board)
                            pygame.display.update()
                        except MoveError as me:
                            continue

            if turn == COMPUTER_TURN and not game_over:
                animation_index = 110
                winning_status, col = self._service.computer_move()

                # drop the piece
                while animation_index < height:
                    self._screen.blit(self._theme.background, (0, 0))
                    animation_index += 1
                    self._screen.blit(self._theme.computer_image, (col * 100 - 100, animation_index))
                    pygame.display.update()
                    clock.tick(500)

                if winning_status == 2:

                    # print wining labels
                    label = self._theme.font.render("LOSER", 1, (255, 255, 0))
                    self._screen.blit(label, (250, 10))

                    # update the board
                    self._draw_board(self._board)
                    self._service.reset()
                    game_over = True

                turn += 1
                turn = turn % 2
                self._draw_board(self._board)

            self._draw_board(self._board)
            pygame.display.update()

        if game_over:
            pygame.time.wait(3000)

    def _draw_board(self, b):
        for col in range(1, COLUMNS + 1):
            for row in range(1, ROWS + 1):
                c = col - 1
                r = row - 1

                if b.data[row][col] == 1:

                    self._screen.blit(self._theme.player_image, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2) - 40,
                                                                 height - int((
                                                                                      ROWS - r - 1) * SQUARE_SIZE + SQUARE_SIZE / 2) - 40))

                if b.data[row][col] == 2:
                    self._screen.blit(self._theme.computer_image, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2) - 40,
                                                                   height - int((
                                                                                        ROWS - r - 1) * SQUARE_SIZE + SQUARE_SIZE / 2) - 40))


def print_data(b):
    for i in b.data:
        print(i)
    print()
