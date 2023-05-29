import typing

from pynput import keyboard as _keyboard

VALUES_KEYS_MAP: typing.Dict[
    str, typing.Dict[str, typing.Union[_keyboard.Key, str]]
] = {"escape": {"key": _keyboard.Key.esc, "value": "escape"}}
