import typing
from enum import StrEnum, auto

from pynput import keyboard as _keyboard

VALUES_KEYS_MAP: typing.Dict[
    str, typing.Dict[str, typing.Union[_keyboard.Key, str]]
] = {
    "escape": {"key": _keyboard.Key.esc, "value": "escape"},
    "enter": {"key": _keyboard.Key.enter, "value": "enter"},
    "arrow-up": {"key": _keyboard.Key.up, "value": "arrow-up"},
    "arrow-down": {"key": _keyboard.Key.down, "value": "arrow-down"},
    "arrow-left": {"key": _keyboard.Key.left, "value": "arrow-left"},
    "arrow-right": {"key": _keyboard.Key.right, "value": "arrow-right"},
}


class GAME_ENGINE_CTX(StrEnum):
    MENU = auto()
    GAME = auto()


class GAME_MENU_CTX(StrEnum):
    MENU = auto()

    # session creation start
    CREATE_NEW_SESSION = (
        CHOOSE_BOARD
    ) = auto()  ## user needs to pick board and difficulty, user_name is picked from cli
    CHOOSE_DIFFICULTY = auto()
    PLAY_NEW = (
        auto()
    )  ## tells game_engine that game_engine.ctx can be moved back to Game_ENGINE_CTX.GAME
    # session creation end

    SAVE_CURRENT_SESSION = (
        auto()
    )  # this is available only if session is created already

    # session load start
    LOAD_SESSION = auto()  # show lists of saves, user can select one and hit enter
    PLAY_LOADED = auto()
    # session load end

    EXIT = auto()


FIELD_TEMPLATE = {
    "display_name": "string",
    "selected": False,
    "next_ctx": None,
    "disabled": False,
}
