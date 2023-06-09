import typing

from pynput import keyboard as _keyboard

from src.constants import KEYS_VALUES_MAP
from src.errors import UnableToRecognizeKey
from src.logging import log_controller_error
from src.utils.abc_utils import ContextManagerAbs
from src.utils.abc_utils import NonBlockingAbs

if typing.TYPE_CHECKING:
    from src.game_engine.game_engine import GameEngine


# TO-DO
# write Your own controller which will take one letter from sys.input
#  and wait based on game frequency
# this way controller won't catch accidential keyboard input
#  from other app


class Controller(ContextManagerAbs, NonBlockingAbs):
    """Takes user input from keyboard and writes it to game engine."""

    # TO-DO
    # do not allow creating of more than one controller

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self._thread = _keyboard.Listener(
            on_press=self.write_key_to_game_engine  # type: ignore [arg-type]
        )

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        if self.is_active():
            self.stop()

    @log_controller_error
    def write_key_to_game_engine(self, key: _keyboard.Key):
        self._write_key_value_to_game_engine(self.game_engine, key)

    @classmethod
    def _write_key_value_to_game_engine(
        cls, game_engine: "GameEngine", key: _keyboard.Key
    ):
        try:
            value = cls._map_key_to_value(key)
        except UnableToRecognizeKey:
            return

        game_engine.user_input.set(value)

    @classmethod
    def _map_key_to_value(cls, key: _keyboard.Key) -> str:
        try:
            return KEYS_VALUES_MAP[key]
        except KeyError:
            raise UnableToRecognizeKey(key)

    def start(self):
        """Controller takes user's input (no-blocking)."""
        self._thread.start()

    def stop(self):
        """Controller doesn't take user's input."""
        self._thread.stop()

    def is_active(self) -> bool:
        """Is controller taking user's input?"""
        return self._thread.running
