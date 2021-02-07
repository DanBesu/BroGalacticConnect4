import random
import sys

import pygame
from pygame import mixer

from src.ui.gui.tools.button import Button
from src.ui.gui.windows.game_gui import TransitionToGame

pygame.init()

ROWS = 6
COLUMNS = 7
SEQUENCE_LENGTH = 4
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 10)
MENU_FONT = pygame.font.SysFont("monospace", 75)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

width_ = COLUMNS * SQUARE_SIZE
height_ = (ROWS + 2) * SQUARE_SIZE
screen_size = (width_, height_)


class MainMenu:

    def __init__(self, game_window, settings_window, service, theme):
        self._game_window = game_window
        self._settings_window = settings_window
        self._game_service = service
        self._game_theme = theme

    def start(self):

        # get the star background
        star_list = []
        for i in range(100):
            x = random.randrange(0, 700)
            y = random.randrange(0, 800)
            star_list.append([x, y])

        screen = pygame.display.set_mode(screen_size)
        transition = TransitionToGame()

        font = pygame.font.SysFont('Corbel', 35)
        start_label = font.render('Start Game', True, (0, 0, 0))
        settings_label = font.render('Settings', True, (0, 0, 0))

        start_button = Button(screen, 210, 234, 300, 60, YELLOW, WHITE, start_label)
        settings_button = Button(screen, 210, 400, 300, 60, YELLOW, WHITE, settings_label)

        title_label = MENU_FONT.render('Welcome', False, WHITE)
        screen.blit(title_label, (40, 10))
        pygame.display.update()

        # background sound
        mixer.music.load(
            'audio/Guardians of the Galaxy Awesome Mix Vol 1 Vol 2 Full Soundtrack13minCompressed (mp3cut.net) (1) (1).wav')
        mixer.music.play(-1)

        clock = pygame.time.Clock()

        while True:

            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_in_button_range(mouse):

                        # set the music for the bro mode
                        if self._game_window.theme.name == 'bro':
                            transition.show(self._game_window.theme.transition_image)
                            mixer.music.load(
                                'audio/50 Cent  In Da Club Intl Version Official Video Compressed(1).wav')
                            mixer.music.play(-1)
                            self._game_window.render_game()
                            mixer.music.load(
                                'audio/Guardians of the Galaxy Awesome Mix Vol 1 Vol 2 Full Soundtrack13minCompressed (mp3cut.net) (1) (1).wav')
                            mixer.music.play(-1)
                        else:
                            transition.show(self._game_window.theme.transition_image)
                            self._game_window.render_game()

                    if settings_button.is_in_button_range(mouse):
                        self._settings_window.open_window()

            screen.fill((60, 25, 60))

            # process star in the list
            for i in range(len(star_list)):

                # draw and move the star
                pygame.draw.circle(screen, YELLOW, star_list[i], 2)
                star_list[i][1] += 1

                # If the star has moved off the bottom of the screen, reset at the top
                if star_list[i][1] > 800:
                    y = random.randrange(-50, -10)
                    star_list[i][1] = y
                    x = random.randrange(0, 700)
                    star_list[i][0] = x

            screen.blit(title_label, (40, 10))
            start_button.draw(mouse)
            settings_button.draw(mouse)

            clock.tick(50)
            # updates the frames of the game
            pygame.display.update()
