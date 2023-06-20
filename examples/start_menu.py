import os
from time import sleep
from random import randint
from unittest.mock import patch, MagicMock

from src.constants import GAME_ENGINE_CTX, SNAKE_DIRECTION
from src.display import BashDisplay
from src.controller import Controller
from src.game_engine.game_engine import GameEngine
from src.game_engine.game_logic.board import BoardNoWalls


def _disable_echoing_input():
    os.system("stty -echo")


def _enable_echoing_input():
    os.system("stty echo")


def _do_not_show_user_input(function):
    def wrapped_function(*args, **kwargs):
        _disable_echoing_input()
        try:
            return function(*args, **kwargs)
        finally:
            _enable_echoing_input()

    return wrapped_function


@_do_not_show_user_input
def main():
    game_engine = GameEngine()

    controller, display = Controller(game_engine), BashDisplay(game_engine)

    game_engine.start()
    controller.start()
    display.start()

    sleep(3000)

    # display.stop()


if __name__ == "__main__":
    main()
