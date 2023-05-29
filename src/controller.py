import typing
import functools

from pynput import keyboard as _keyboard

from src.constants import VALUES_KEYS_MAP
from src.user_input import UserInput
from src.errors import UnableToRecognizeKey


def _does_thread_exsist(obj: typing.Any) -> bool:
    return getattr(obj, "_thread") is not None


class _validate_thread_exsists:
    """ Decorator whih cheks `cls._thread` exsistance. """

    def __init__(self, should_exsists: bool):
        self.should_exsists = should_exsists

    def __call__(self, function):
        @functools.wraps(function)
        def wrapper(cls, *args, **kwargs):
            thread_exsists = _does_thread_exsist(cls)

            if thread_exsists is not self.should_exsists:
                raise NotImplementedError(cls, *args, **kwargs)

            return function(cls, *args, **kwargs)

        return wrapper


class Controller:
    """ Take's user input in seperate thread. """

    _thread: typing.Optional[_keyboard.Listener] = None

    def __init__(self, game_engine):
        self.game_engine = game_engine

    def __enter__(self):
        if not self.does_thread_exsists():
            self.start(self.game_engine)

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        try:
            if self.is_active():
                self.stop()
        finally:
            self.cleanup()

    @classmethod
    def _write_key_value_to_game_engine(cls, game_engine, key):
        try:
            value = cls.map_key_to_value(key)
        except UnableToRecognizeKey:
            return

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
        """Take user's input as a keyboard key and transform it to form
        understandable by game engine. This is sth like peripheral abstraction."""

        def write_key_to_game_engine(key):
            cls._write_key_value_to_game_engine(game_engine, key)

        def create_thread():
            return _keyboard.Listener(on_press=write_key_to_game_engine)

        thread = create_thread()

        thread.start()

        cls._thread = thread

    @classmethod
    @_validate_thread_exsists(True)
    def stop(cls):
        cls._thread.stop()

    @classmethod
    @_validate_thread_exsists(True)
    def cleanup(cls):
        cls._thread = None

    @classmethod
    @_validate_thread_exsists(True)
    def is_active(cls) -> bool:
        return cls._thread.running

    @classmethod
    def does_thread_exsists(cls) -> bool:
        return _does_thread_exsist(cls)
