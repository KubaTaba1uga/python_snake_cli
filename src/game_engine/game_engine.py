import typing
from threading import Thread
from time import sleep

from src.constants import DEFAULT_GAME_FREQUENCY_IN_HZ
from src.constants import GAME_ENGINE_CTX
from src.constants import get_key_value_by_display_name
from src.constants import SNAKE_DIRECTION
from src.errors import SnakeDied
from src.game_engine.game_menu import GameMenu
from src.game_engine.session import Session
from src.game_engine.utils.si_utils import get_seconds_from_hz
from src.logging import log_game_engine_error
from src.user_input import UserInput


def _manage_game_menu_and_session(function) -> typing.Any:
    """Manages the current session or creates a new one.
    Makes sure that game_menu is always available."""

    def wrapped_func(self: "GameEngine", *args, **kwargs):
        result = function(self, *args, **kwargs)

        if self.game_menu.is_session_ready():
            self.ctx = GAME_ENGINE_CTX.GAME

            self.game_menu = GameMenu(self.session)

        return result

    return wrapped_func


def _go_back_to_menu_if_snake_dead(function) -> typing.Any:
    """Makes sure that game won't crash when snake is dead.
    Instead go back to menu and show game results."""

    def wrapped_func(self: "GameEngine", *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except SnakeDied:
            self.game_menu.loose_session()

            sleep(1)  # let user watch the failure

            self.ctx = GAME_ENGINE_CTX.MENU

    return wrapped_func


# TO-DO
#  session keeps board & snake
class GameEngine:
    DEFAULT_USER_INPUT_VALUE = "None"

    # Game has to start from menu to load first session
    DEFAULT_GAME_ENGINE_CTX = GAME_ENGINE_CTX.MENU

    DEFAULT_FREQ_IN_HZ = DEFAULT_GAME_FREQUENCY_IN_HZ

    @classmethod
    def sleep(cls):
        sleep(get_seconds_from_hz(cls.DEFAULT_FREQ_IN_HZ))

    @property
    def board(self):
        return self.session.board

    @property
    def session(self) -> Session:
        return self.game_menu.session

    def __init__(self):
        self.user_input: UserInput = UserInput(self.DEFAULT_USER_INPUT_VALUE)
        self.ctx: GAME_ENGINE_CTX = self.DEFAULT_GAME_ENGINE_CTX
        self.game_menu: GameMenu = GameMenu()

        self._thread: Thread = Thread(target=self._process_game_engine)

        self.GAME_USER_INPUT_FUNC_MAP = self._init_game_user_input_func_map()
        self.PAUSE_USER_INPUT_FUNC_MAP = self._init_pause_user_input_func_map()

    def _init_game_user_input_func_map(self) -> typing.Dict[str, typing.Callable]:
        def pause_game():
            self.ctx = GAME_ENGINE_CTX.PAUSE

        return {
            get_key_value_by_display_name(
                "UP ARROW key"
            ): lambda: self.board.snake.set_direction(SNAKE_DIRECTION.UP),
            get_key_value_by_display_name(
                "DOWN ARROW key"
            ): lambda: self.board.snake.set_direction(SNAKE_DIRECTION.DOWN),
            get_key_value_by_display_name(
                "LEFT ARROW key"
            ): lambda: self.board.snake.set_direction(SNAKE_DIRECTION.LEFT),
            get_key_value_by_display_name(
                "RIGHT ARROW key"
            ): lambda: self.board.snake.set_direction(SNAKE_DIRECTION.RIGHT),
            get_key_value_by_display_name("p key"): pause_game,
        }

    def _init_pause_user_input_func_map(self) -> typing.Dict[str, typing.Callable]:
        def unpause_game():
            self.ctx = GAME_ENGINE_CTX.GAME

        return {get_key_value_by_display_name("p key"): unpause_game}

    def start(self):
        self._thread.start()

    @log_game_engine_error
    def _process_game_engine(self):
        while True:
            self._process()
            self.sleep()

    def _process(self):
        self._process_user_input()
        self._process_ctx()

    def _process_user_input(self):
        USER_INPUT_PROCESS_FUNC_MAP = {
            GAME_ENGINE_CTX.MENU: self.game_menu.USER_INPUT_FUNC_MAP,
            GAME_ENGINE_CTX.GAME: self.GAME_USER_INPUT_FUNC_MAP,
            GAME_ENGINE_CTX.PAUSE: self.PAUSE_USER_INPUT_FUNC_MAP,
        }

        try:
            USER_INPUT_PROCESS_FUNC_MAP[self.ctx][self.user_input.get()]()
        except KeyError:
            pass

        self.user_input.set(self.DEFAULT_USER_INPUT_VALUE)

    def _process_ctx(self):
        GAME_ENGINE_CTX_PROCESS_FUNC_MAP = {
            GAME_ENGINE_CTX.MENU: self._process_menu_ctx,
            GAME_ENGINE_CTX.GAME: self._process_game_ctx,
            GAME_ENGINE_CTX.PAUSE: self._process_pause_ctx,
        }

        GAME_ENGINE_CTX_PROCESS_FUNC_MAP[self.ctx]()

    @_manage_game_menu_and_session
    def _process_menu_ctx(self):
        self.game_menu.process_ctx()

    @_go_back_to_menu_if_snake_dead
    def _process_game_ctx(self):
        """Performs game logic."""
        self.board.process()

    def _process_pause_ctx(self):
        """Do nothing."""
        pass
