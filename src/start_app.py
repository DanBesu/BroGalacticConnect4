import pygame

from src import settings
from src.domain.board import Board
from src.service.game_service import GameService
from src.ui.console_ui.game_ui import MainMenuUI, GameUI, SettingsUI
from src.ui.console_ui.run_menu import GameRunner
from src.ui.gui.windows.main_menu_window import MainMenu
from src.ui.gui.tools.theme import Theme
from src.ui.gui.windows.game_gui import GameWindow
from src.ui.gui.windows.settings_window import SettingsWindow


class ConfigureSettings:

    def __init__(self):
        self._ui_config = settings.ui

    def start_program(self):

        board = Board()
        game_service = GameService(board)

        if self._ui_config == 'console':

            # console ui
            main_menu_ui = MainMenuUI()
            game_ui = GameUI(game_service)
            settings_ui = SettingsUI(game_service)

            game = GameRunner(main_menu_ui, game_ui, settings_ui)
            game.run_main_menu()

        elif self._ui_config == 'GUI':

            # gui
            pygame.init()
            theme = Theme()

            game_gui = GameWindow(game_service, theme)
            settings_window = SettingsWindow(game_gui, game_service)

            main_menu = MainMenu(game_gui, settings_window, game_service, theme)
            main_menu.start()


application_configurations = ConfigureSettings()
application_configurations.start_program()
