from unittest.mock import MagicMock

import pytest

from src.constants import GAME_ENGINE_CTX
from src.game_engine.game_engine import GameEngine
from src.game_engine.game_logic.board import BoardNoWalls


@pytest.fixture
def game_engine_menu():
    game_engine = GameEngine()
    game_engine.ctx = GAME_ENGINE_CTX.MENU

    return game_engine


@pytest.fixture
def game_engine_game():
    game_engine = GameEngine()
    game_engine.ctx = GAME_ENGINE_CTX.GAME

    board = BoardNoWalls(width=5, height=5)

    session = MagicMock(board=board)

    game_engine._session = session

    return game_engine


@pytest.fixture
def board_no_walls_square():
    return BoardNoWalls(5, 5)


@pytest.fixture
def board_no_walls_rect():
    return BoardNoWalls(10, 5)
