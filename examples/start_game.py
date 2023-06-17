from time import sleep
from random import randint
from unittest.mock import patch, MagicMock

from src.constants import GAME_ENGINE_CTX, SNAKE_DIRECTION
from src.display import BashDisplay
from src.controller import Controller
from src.game_engine.game_engine import GameEngine
from src.game_engine.game_logic.board import BoardNoWalls


SNAKE_MOVES = [move for move in SNAKE_DIRECTION]


def main():
    game_engine = GameEngine()

    controller, display = Controller(game_engine), BashDisplay(game_engine)

    board = BoardNoWalls(10)

    session = MagicMock(board=board)

    game_engine._session = session

    game_engine.ctx = GAME_ENGINE_CTX.GAME
    game_engine.start()
    controller.start()
    display.start()

    sleep(1000)

    controller.stop()
    display.stop()
    # game_engine.stop()


if __name__ == "__main__":
    main()
