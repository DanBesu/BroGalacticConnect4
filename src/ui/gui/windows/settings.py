
import pygame

from src.ui.gui.tools.button import Button
from src.ui.gui.tools.theme import Theme

SCREEN_SIZE = (700, 700)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


class SettingsWindow:

    def __init__(self, game_window, game_service):
        self._game_window = game_window
        self._game_service = game_service

        # build the bro theme
        background = pygame.image.load('D:/CODE/GitFaculty/a11-DanBesu/bombardier.jpg')
        boss = pygame.image.load('D:/CODE/GitFaculty/a11-DanBesu/bossc.png')
        paul = pygame.image.load('D:/CODE/GitFaculty/a11-DanBesu/paulc.png')
        monospace_font = pygame.font.SysFont("monospace", 75)
        self._bro_theme = Theme(background, boss, paul, monospace_font)

        # build the galactic theme
        background = pygame.image.load('D:/CODE/GitFaculty/a11-DanBesu/galactic_background.jpg')
        boss = pygame.image.load('D:/CODE/GitFaculty/a11-DanBesu/doodle.png')
        paul = pygame.image.load('D:/CODE/GitFaculty/a11-DanBesu/paulc.png')
        monospace_font = pygame.font.SysFont("monospace", 75)
        self._galactic_theme = Theme(background, boss, paul, monospace_font)

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

        # set theme button labels
        button_font = pygame.font.SysFont("monospace", 25)
        gang_label = button_font.render('bro mode', True, BLACK)  # theme labels
        galactic_label = button_font.render('galactic mode', True, BLACK)
        easy_label = button_font.render('easy', True, BLACK)
        medium_label = button_font.render('easy', True, BLACK)
        hard_label = button_font.render('easy', True, BLACK)
        dangerous_label = button_font.render('easy', True, BLACK)

        # set theme buttons
        bro_theme_button = Button(screen, 100, 234, 150, 30, YELLOW, WHITE, gang_label)
        galactic_theme_button = Button(screen, 500, 234, 150, 30, YELLOW, WHITE, galactic_label)

        pygame.display.update()

        open_ = True
        while open_:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    open_ = False
                if bro_theme_button.is_in_button_range(mouse):
                    self.__set_bro_theme()
                if galactic_theme_button.is_in_button_range(mouse):
                    self.__set_galactic_theme()

            mouse = pygame.mouse.get_pos()
            screen.fill((60, 25, 60))
            screen.blit(title_label, (40, 10))
            bro_theme_button.draw(mouse)
            galactic_theme_button.draw(mouse)
            pygame.display.update()
