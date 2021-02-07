import random

import pygame

from src.ui.gui.tools.button import Button
from src.ui.gui.tools.theme import Theme

SCREEN_SIZE = (700, 800)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()


class SettingsWindow:

    def __init__(self, game_window, game_service):
        self._game_window = game_window
        self._game_service = game_service

        # build the bro theme
        background = pygame.image.load('images/bombardier700800.jpeg')
        boss = pygame.image.load('images/bossc.png')
        paul = pygame.image.load('images/paulc.png')
        monospace_font = pygame.font.SysFont("images/monospace", 75)
        transition_image = pygame.image.load('images/bro_transition.jpeg')
        self._bro_theme = Theme('bro', background, boss, paul, monospace_font, transition_image)

        # build the galactic theme
        background = pygame.image.load('images/galaxy_background.jpeg')
        boss = pygame.image.load('images/tesla_cut.png')
        paul = pygame.image.load('images/ufo_cut.png')
        monospace_font = pygame.font.SysFont("paladins", 75)
        transition_image = pygame.image.load('images/galaxy_transition.jpeg')
        self._galactic_theme = Theme('galactic', background, boss, paul, monospace_font, transition_image)

    def __set_bro_theme(self):
        self._game_window.theme = self._bro_theme

    def __set_galactic_theme(self):
        self._game_window.theme = self._galactic_theme

    def __set_difficulty(self, difficulty):
        self._game_service.difficulty = difficulty

    def open_window(self):

        # initialise the screen
        screen = pygame.display.set_mode(SCREEN_SIZE)
        screen.fill((60, 25, 60))

        # set the title
        title_font = pygame.font.SysFont("monospace", 75)
        title_label = title_font.render('Settings', False, WHITE)
        screen.blit(title_label, (40, 10))

        button_font = pygame.font.SysFont("monospace", 25)

        # set theme button labels
        theme_label = button_font.render('Taste:', True, WHITE)
        bro_label = button_font.render('bro mode', True, BLACK)
        galactic_label = button_font.render('galactic mode', True, BLACK)

        # set theme buttons
        bro_theme_button = Button(screen, 100, 234, 150, 30, YELLOW, WHITE, bro_label)
        galactic_theme_button = Button(screen, 350, 234, 200, 30, YELLOW, WHITE, galactic_label)

        # set difficulty labels
        difficulty_label = button_font.render('IQ Range:', True, WHITE)
        easy_label = button_font.render('babycandy', True, BLACK)
        medium_label = button_font.render('casual', True, BLACK)
        hard_label = button_font.render('insane', True, BLACK)
        ai_label = button_font.render('warzone', True, BLACK)

        # set difficulty buttons
        easy_button = Button(screen, 50, 520, 150, 30, YELLOW, WHITE, easy_label)
        medium_button = Button(screen, 230, 520, 100, 30, YELLOW, WHITE, medium_label)
        hard_button = Button(screen, 400, 520, 100, 30, YELLOW, WHITE, hard_label)
        ai_button = Button(screen, 550, 520, 110, 30, YELLOW, WHITE, ai_label)

        # get the star background
        star_list = []
        for i in range(50):
            x = random.randrange(0, 700)
            y = random.randrange(0, 800)
            star_list.append([x, y])

        pygame.display.update()

        open_ = True
        while open_:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    open_ = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bro_theme_button.is_in_button_range(mouse):
                        self.__set_bro_theme()
                    if galactic_theme_button.is_in_button_range(mouse):
                        self.__set_galactic_theme()
                    if easy_button.is_in_button_range(mouse):
                        self.__set_difficulty(1)
                    if medium_button.is_in_button_range(mouse):
                        self.__set_difficulty(2)
                    if hard_button.is_in_button_range(mouse):
                        self.__set_difficulty(3)
                    if ai_button.is_in_button_range(mouse):
                        self.__set_difficulty(4)

            # update the screen
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

            mouse = pygame.mouse.get_pos()
            screen.blit(title_label, (40, 10))

            # draw theme zone
            screen.blit(theme_label, (200, 160))
            bro_theme_button.draw(mouse)
            galactic_theme_button.draw(mouse)
            screen.blit(self._bro_theme.player_image, (95, 280))
            screen.blit(self._bro_theme.computer_image, (175, 280))
            screen.blit(self._galactic_theme.player_image, (370, 280))
            screen.blit(self._galactic_theme.computer_image, (460, 280))

            # draw difficulty zone
            screen.blit(difficulty_label, (160, 440))
            easy_button.draw(mouse)
            medium_button.draw(mouse)
            hard_button.draw(mouse)
            ai_button.draw(mouse)

            clock.tick(50)
            pygame.display.update()


