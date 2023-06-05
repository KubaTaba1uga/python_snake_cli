import typing

from time import sleep

from src.user_input import UserInput
from src.constants import GAME_ENGINE_CTX, GAME_MENU_CTX
from src.game_engine.game_menu import GameMenu
from src.game_engine.utils.si_utils import get_seconds_from_hz


def _manage_game_menu_and_session(function):
    """Manages the current session or creates a new one.
    Makes sure that game_menu is always available."""

    def wrapped_func(self, *args, **kwargs):

        if self.game_menu is None:
            self.game_menu = GameMenu(self._session)

        result = function(self, *args, **kwargs)

        if self.game_menu.is_session_ready():
            self._session = self.game_menu.session
            self.game_menu = None

        return result

    return wrapped_func


# TO-DO
#  less internal states usage, more passing as argument -> more @classmethod and interfaes to them
#  session keeps board & snake
class GameEngine:
    DEFAULT_USER_INPUT_VALUE = "None"

    # Game has to start from menu to load first session
    DEFAULT_GAME_ENGINE_CTX = GAME_ENGINE_CTX.MENU

    DEFAULT_FREQ_IN_HZ = 1

    @classmethod
    def sleep(cls):
        sleep(get_seconds_from_hz(cls.DEFAULT_FREQ_IN_HZ))

    def __init__(self):
        self.user_input: UserInput = UserInput(self.DEFAULT_USER_INPUT_VALUE)
        self.ctx: GAME_ENGINE_CTX = self.DEFAULT_GAME_ENGINE_CTX
        self.game_menu: GameMenu = GameMenu()

        self._session = None

    def _start(self):
        while True:
            self._process()
            self.sleep()

    @_manage_game_menu_and_session
    def _process(self):
        self._process_user_input()
        self._process_ctx()

    def _process_user_input(self):
        USER_INPUT_PROCESS_FUNC_MAP = {
            GAME_ENGINE_CTX.MENU: self.game_menu.USER_INPUT_FUNC_MAP,
            GAME_ENGINE_CTX.GAME: self.USER_INPUT_FUNC_MAP,
        }

        USER_INPUT_PROCESS_FUNC_MAP[self.ctx][self.user_input.value]()

    def _process_ctx(self):
        GAME_ENGINE_CTX_PROCESS_FUNC_MAP = {
            GAME_ENGINE_CTX.MENU: self._process_menu_ctx,
            GAME_ENGINE_CTX.GAME: self._process_game_ctx,
        }

        GAME_ENGINE_CTX_PROCESS_FUNC_MAP[self.ctx]()

    def _process_menu_ctx(self):
        self.game_menu.process_ctx()

    def _process_game_ctx(self):
        """ Performs game logic. """
        # add game logi here
        raise NotImplementedError(self)
