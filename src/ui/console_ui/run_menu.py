from src.service.game_service import MoveError
from src.ui.console_ui.game_ui import SettingsInputError


class GameRunner:

    def __init__(self, main_menu_ui, game_ui, settings_ui):
        self._main_menu_ui = main_menu_ui
        self._game_ui = game_ui
        self._settings_ui = settings_ui

    def run_main_menu(self):

        command_dict = {'0': self._main_menu_ui.exit, '1': self.__run_game, '2': self.__run_settings}
        self._main_menu_ui.display()

        while True:
            command = input('What u gonna do: ')
            command.strip()
            if command in command_dict:
                command_dict[command]()
                self._main_menu_ui.display()
            else:
                print('invalid input')

    def __run_game(self):
        while True:
            self._game_ui.display_board()
            status = get_handled_input(self._game_ui.move_ui, MoveError, 1)
            if status is True:
                break  # go back by printing the main menu in the main loop (run_main_menu)
            status = self._game_ui.move_ui(2)
            if status is True:
                break  # go back by printing the main menu in the main loop (run_main_menu)

    def __run_settings(self):
        command_dict = {'1': self._settings_ui.input_players,
                        '2': self._settings_ui.input_difficulty}

        self._settings_ui.display()
        while True:
            command = input('... ')
            if command in command_dict:
                get_handled_input(command_dict[command], SettingsInputError)
                self._settings_ui.display()
            elif command == '0':
                print('see u on the battlefield!')
                break  # go back by printing the main menu in the main loop
            else:
                print('there is no such command in the settings menu')


def get_handled_input(input_function, exception, *params):
    while True:
        try:
            return input_function(*params)
        except exception as e:
            print(e)
