import typing
from abc import abstractclassmethod
from time import sleep

from src.constants import GAME_ENGINE_CTX
from src.game_engine.utils.si_utils import get_seconds_from_hz

if typing.TYPE_CHECKING:
    from src.game_engine.game_menu import GameMenu
    from src.game_engine.game_engine import GameEngine


class DisplayAbs:
    DEFAULT_FREQ_IN_HZ = 1

    @classmethod
    def sleep(cls):
        sleep(get_seconds_from_hz(cls.DEFAULT_FREQ_IN_HZ))

    def __init__(self, game_engine: "GameEngine"):
        self._game_engine: "GameEngine" = game_engine

    @abstractclassmethod
    def render_game_menu(cls, game_engine: "GameEngine"):
        """ Display game's menu. GameEngine """
        pass

    @abstractclassmethod
    def render_game_engine(cls, game_engine: "GameEngine"):
        """ Display gameplay. """
        pass

    @classmethod
    def _render(cls, game_engine: "GameEngine"):
        CTX_RENDER_MAP = {
            GAME_ENGINE_CTX.GAME: cls.render_game_engine,
            GAME_ENGINE_CTX.MENU: cls.render_game_menu,
        }

        CTX_RENDER_MAP[game_engine.ctx](game_engine)

    def render(self):
        self._render(self._game_engine)
