import typing
from enum import auto
from enum import StrEnum

from pynput import keyboard as _keyboard

# Please do not use pynupt directly.

# Interface to pynput keys values
KEYS_VALUES_MAP: typing.Dict[_keyboard.Key, str] = {
    _keyboard.Key.esc: "escape",
    _keyboard.Key.enter: "enter",
    _keyboard.Key.up: "arrow-up",
    _keyboard.Key.down: "arrow-down",
    _keyboard.Key.left: "arrow-left",
    _keyboard.Key.right: "arrow-right",
}

# Interface to pynput keys
DISPLAY_NAMES_KEYS_MAP: typing.Dict[str, _keyboard.Key] = {
    "ESC key": _keyboard.Key.esc,
    "ENTER key": _keyboard.Key.enter,
    "UP ARROW key": _keyboard.Key.up,
    "DOWN ARROW key": _keyboard.Key.down,
    "LEFT ARROW key": _keyboard.Key.left,
    "RIGHT ARROW key": _keyboard.Key.right,
}


class GAME_ENGINE_CTX(StrEnum):
    MENU = auto()
    GAME = auto()


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

    EXIT = auto()


class BoardFieldType(StrEnum):
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


class SnakeDirection(StrEnum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def get_key_value_by_display_name(key_display_name: str) -> str:
    return KEYS_VALUES_MAP[DISPLAY_NAMES_KEYS_MAP[key_display_name]]
