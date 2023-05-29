import typing
import functools

from pynput import keyboard as _keyboard

from src.constants import VALUES_KEYS_MAP
from src.user_input import UserInput
from src.errors import UnableToRecognizeKey


class _validate_thread_exsists:
    """ Decorator whih cheks `cls._thread` exsistance. """

    def __init__(self, exsists):
        self.exsists = exsists

    def __call__(self, function):
        @functools.wraps(function)
        def wrapper(cls, *args, **kwargs):
            thread_exsists = cls._thread is not None

            if thread_exsists is not self.exsists:
                raise NotImplementedError(cls, *args, **kwargs)

            print(args)

            return function(cls, *args, **kwargs)

        return wrapper


class Controller:
    """ Take's user input in seperate thread. """

    _thread: typing.Optional[_keyboard.Listener] = None

    @classmethod
    def _write_key_to_game_engine(cls, game_engine, key):
        try:
            value = cls.map_key_to_value(key)
        except UnableToRecognizeKey:
            return

        print("AAA:", value)

        game_engine.user_input.set(value)

    @classmethod
    def map_key_to_value(cls, key) -> str:
        for value_key_map in VALUES_KEYS_MAP.values():
            if key is value_key_map["key"]:
                return value_key_map["value"]

        raise UnableToRecognizeKey(key)

    @classmethod
    @_validate_thread_exsists(False)
    def start(cls, game_engine):
        " Start a thread which will take user's input. "

        def write_key_to_game_engine(key):
            cls._write_key_to_game_engine(game_engine, key)

        thread = _keyboard.Listener(on_press=write_key_to_game_engine)

        thread.start()

        cls._thread = thread

    @classmethod
    @_validate_thread_exsists(True)
    def stop(cls):
        cls._thread.stop()
