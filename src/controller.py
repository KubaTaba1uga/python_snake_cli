import typing
from dataclasses import dataclass

from pynput import keyboard as _keyboard

from src.constants import VALUES_KEYS_MAP


@dataclass
class UserInput:
    _value: int

    def write(self, value):
        self._value = value

    def get(self):
        return self._value


class Controller:
    """ Take's user input in seperate thread. """

    _thread: typing.Optional[_keyboard.Listener] = None

    @classmethod
    def _write_key_to_game_engine(cls, game_engine, key):
        value = cls.map_key_to_value(key)
        game_engine.user_input.write(value)

    @classmethod
    def _validate_thread_not_exsist(cls, func):
        if cls._thread is not None:
            raise NotImplementedError()

    @classmethod
    def map_key_to_value(cls, key) -> bool:
        for value, local_key in VALUES_KEYS_MAP.items():
            if key is local_key:
                return value

        raise NotImplementedError(key, VALUES_KEYS_MAP)

    @classmethod
    def start(cls, game_engine):
        " Start a thread which will take user's input. "
        attr_to_write_to: UserInput = game_engine.user_input

        def write_key_to_game_engine(key):
            cls._write_key_to_game_engine(game_engine, key)

        thread = _keyboard.Listener(on_press=write_key_to_game_engine)

        thread.start()

        cls._thread = thread

    @classmethod
    def stop(cls):
        cls._thread.stop()
