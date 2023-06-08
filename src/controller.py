import functools
import typing

from pynput import keyboard as _keyboard

from src.constants import KEYS_VALUES_MAP
from src.errors import PleaseUseContextManagerError
from src.errors import UnableToRecognizeKey
from src.utils.abc_utils import ContextManagerAbs, NonBlockingAbs

if typing.TYPE_CHECKING:
    from src.game_engine.game_engine import GameEngine


class Controller(ContextManagerAbs, NonBlockingAbs):
    """ Takes user input from keyboard and writes it to game engine. """

    # TO-DO
    # do not allow creating of more than one controller

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self._thread = _keyboard.Listener(on_press=self._write_key_to_game_engine)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        if self.is_active():
            self.stop()

    @classmethod
    def _write_key_value_to_game_engine(
        cls, game_engine: "GameEngine", key: _keyboard.Key
    ):
        try:
            value = cls.map_key_to_value(key)
        except UnableToRecognizeKey:
            return

        game_engine.user_input.set(value)

    @classmethod
    def _map_key_to_value(cls, key: _keyboard.Key) -> str:
        try:
            return KEYS_VALUES_MAP[key]
        except KeyError:
            raise UnableToRecognizeKey(key)

    def _write_key_to_game_engine(self, key):
        self._write_key_value_to_game_engine(self.game_engine, key)

    def start(self):
        """ Controller takes user's input (no-blocking). """
        self._thread.start()

    def stop(self):
        """ Controller doesn't take user's input. """
        self._thread.stop()

    def is_active(self) -> bool:
        """ Does controller take user's input? """
        return self._thread.running
