import typing
from enum import auto
from enum import StrEnum
from pathlib import Path

from pynput import keyboard as _keyboard

# Please do not use pynupt directly.

# Interface to pynput keys values
KEYS_VALUES_MAP: typing.Dict[typing.Union[_keyboard.Key, _keyboard.KeyCode], str] = {
    _keyboard.Key.esc: "escape",
    _keyboard.Key.enter: "enter",
    _keyboard.Key.up: "arrow-up",
    _keyboard.Key.down: "arrow-down",
    _keyboard.Key.left: "arrow-left",
    _keyboard.Key.right: "arrow-right",
    _keyboard.KeyCode(char="p"): "p",
}

# Interface to pynput keys
DISPLAY_NAMES_KEYS_MAP: typing.Dict[
    str, typing.Union[_keyboard.Key, _keyboard.KeyCode]
] = {
    "ESC key": _keyboard.Key.esc,
    "ENTER key": _keyboard.Key.enter,
    "UP ARROW key": _keyboard.Key.up,
    "DOWN ARROW key": _keyboard.Key.down,
    "LEFT ARROW key": _keyboard.Key.left,
    "RIGHT ARROW key": _keyboard.Key.right,
    "p key": _keyboard.KeyCode(char="p"),
}


class GAME_ENGINE_CTX(StrEnum):
    MENU = auto()
    GAME = auto()
    PAUSE = auto()


class GAME_MENU_CTX(StrEnum):
    MENU = auto()

    # session creation start
    CHOOSE_BOARD = auto()
    CHOOSE_SIZE = auto()
    CHOOSE_DIFFICULTY = auto()
    PLAY_NEW = auto()  ## tells game_engine that game_engine.ctx
    ##                     can be moved back to Game_ENGINE_CTX.GAME
    # session creation end

    SAVE_CURRENT_SESSION = (
        auto()
    )  # this is available only if session is created already

    # session load start
    LOAD_SESSION = auto()  # show lists of saves, user can select one and hit enter
    PLAY_LOADED = auto()
    # session load end

    SHOW_SESSION = auto()

    PLAY_END = auto()

    EXIT = auto()


class BOARD_FIELD_TYPE(StrEnum):
    WALL = auto()
    SNAKE = auto()
    FRUIT = auto()
    GROUND = auto()


FIELD_TEMPLATE = {
    "display_name": "string",
    "selected": False,
    "next_ctx": None,
    "disabled": False,
}


class SNAKE_DIRECTION(StrEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def get_key_value_by_display_name(key_display_name: str) -> str:
    return KEYS_VALUES_MAP[DISPLAY_NAMES_KEYS_MAP[key_display_name]]


# do not change this value please!
DEFAULT_GAME_FREQUENCY_IN_HZ = 100

LOGS_DIR = Path(__file__).parent.parent.joinpath("logs")
