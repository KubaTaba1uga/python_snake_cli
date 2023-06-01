import typing
from enum import StrEnum, auto

from pynput import keyboard as _keyboard

VALUES_KEYS_MAP: typing.Dict[
    str, typing.Dict[str, typing.Union[_keyboard.Key, str]]
] = {"escape": {"key": _keyboard.Key.esc, "value": "escape"}}


class GAME_ENGINE_CTX(StrEnum):
    MENU = auto()
    GAME = auto()


class GAME_MENU_CTX(StrEnum):
    MENU = auto()

    # session creation start
    CREATE_NEW_SESSION = (
        auto()
    )  # user needs to pick board and difficulty, user_name is picked from cli
    CHOOSE_BOARD = auto()
    CHOOSE_DIFFICULTY = auto()
    # session creation end

    SAVE_CURRENT_SESSION = (
        auto()
    )  # this is available only if session is created already

    LOAD_SESSION = auto()  # show lists of saves, user can select one and hit enter

    EXIT = auto()
